"""p2 S3 Object views"""
from time import sleep, time
from uuid import uuid4
from xml.etree import ElementTree

from django.http.response import HttpResponse, StreamingHttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.components.expire.constants import TAG_EXPIRE_DATE
from p2.core.models import Blob
from p2.core.constants import ATTR_BLOB_HASH_MD5
from p2.core.prefix_helper import make_absolute_path
from p2.lib.shortcuts import get_list_for_user_or_404
from p2.s3.constants import (TAG_S3_MULTIPART_BLOB_PART,
                             TAG_S3_MULTIPART_BLOB_TARGET_BLOB,
                             TAG_S3_MULTIPART_BLOB_UPLOAD_ID, XML_NAMESPACE)
from p2.s3.http import XMLResponse
from p2.s3.tasks import complete_multipart_upload
from p2.s3.views.common import S3View

DEFAULT_BLOB_EXPIRY = 86400


class MultipartUploadView(S3View):
    """Multipart-Object related views"""

    volume = None
    request = None

    def dispatch(self, request, bucket, path):
        """Preflight checks"""
        self.request = request
        self.volume = self.get_volume('use_volume', name=bucket)
        return super().dispatch(request, bucket, path)

    ## HTTP Method handlers

    def post(self, request, bucket, path):
        """Post handler"""
        # If 'uploadId' Parameter is set, we should close the upload
        if 'uploadId' in request.GET:
            return self.post_handle_mp_complete(request, self.volume, path)
        return self.post_handle_mp_initiate(request, self.volume, path)

    ## API Handlers

    def post_handle_mp_complete(self, request, volume, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadComplete.html"""
        upload_id = request.GET.get('uploadId')
        # Ensure Multipart upload has started, otherwise 404
        get_list_for_user_or_404(request.user, 'p2_core.change_blob', **{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'volume': self.volume
        })

        def generator():
            """start task, generating spaces to keep connection alive"""
            yield '<?xml version="1.0" encoding="utf8"?>'  # Yield XML Header
            task = complete_multipart_upload.delay(
                upload_id=upload_id,
                user_pk=request.user.pk,
                volume_pk=self.volume.pk,
                path=path
            )
            while not task.ready():
                yield ' ' # Yield space to keep connection alive
                sleep(0.5)
            yield task.get()
        return StreamingHttpResponse(generator(), content_type='text/xml')

    def post_handle_mp_initiate(self, request, volume, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadInitiate.html"""
        # Check if an existing Multipart Upload exists
        existing = get_objects_for_user(request.user, 'p2_core.change_blob').filter(**{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'volume': self.volume
        })
        root = ElementTree.Element("{%s}InitiateMultipartUploadResult" % XML_NAMESPACE)
        ElementTree.SubElement(root, "Bucket").text = self.volume.name
        ElementTree.SubElement(root, "Key").text = path.lstrip('/')
        upload_id = uuid4().hex
        if existing.exists():
            blob = existing.first()
        else:
            blob = Blob.objects.create(
                path=make_absolute_path("/%s_%s/part_%d" % (path, upload_id, 1)),
                volume=self.volume,
                tags={
                    TAG_S3_MULTIPART_BLOB_PART: 1,
                    TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
                    TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
                    TAG_EXPIRE_DATE: time() + DEFAULT_BLOB_EXPIRY,
                }
            )
            assign_perm('p2_core.change_blob', request.user, blob)
        ElementTree.SubElement(root, "UploadId").text = blob.tags[TAG_S3_MULTIPART_BLOB_UPLOAD_ID]
        return XMLResponse(root)

    def put(self, request, volume, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadUploadPart.html"""
        upload_id = request.GET.get('uploadId')
        part_number = int(request.GET.get('partNumber'))
        # Ensure Multipart upload has started, otherwise 404
        get_list_for_user_or_404(request.user, 'p2_core.change_blob', **{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'volume': self.volume
        })
        # Create new Upload part, or reuse existing part and overwrite data
        parts = get_objects_for_user(request.user, 'p2_core.change_blob').filter(**{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_PART: part_number,
            'volume': self.volume
        })
        if parts.exists():
            blob = parts.first()
        else:
            blob = Blob.objects.create(
                path=make_absolute_path("/%s_%s/part_%d" % (path, upload_id, part_number)),
                volume=self.volume,
                tags={
                    TAG_S3_MULTIPART_BLOB_PART: part_number,
                    TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
                    TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
                    TAG_EXPIRE_DATE: time() + DEFAULT_BLOB_EXPIRY,
                }
            )
            assign_perm('p2_core.change_blob', request.user, blob)
        blob.write(request.body)
        blob.save()
        # This response needs an ETag
        response = HttpResponse(status=200)
        response['ETag'] = blob.attributes.get(ATTR_BLOB_HASH_MD5)
        return response
