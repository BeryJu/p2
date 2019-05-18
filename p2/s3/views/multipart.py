"""p2 S3 Object views"""
from time import sleep
from uuid import uuid4
from xml.etree import ElementTree

from django.http.response import HttpResponse, StreamingHttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.models import Blob, Volume
from p2.lib.shortcuts import get_list_for_user_or_404
from p2.s3.auth import S3Authentication
from p2.s3.constants import (TAG_S3_MULTIPART_BLOB_PART,
                             TAG_S3_MULTIPART_BLOB_TARGET_BLOB,
                             TAG_S3_MULTIPART_BLOB_UPLOAD_ID, XML_NAMESPACE,
                             ErrorCodes)
from p2.s3.http import XMLResponse
from p2.s3.tasks import complete_multipart_upload


class MultipartUploadView(S3Authentication):
    """Multipart-Object related views"""

    ## HTTP Method handlers

    def post(self, request, bucket, path):
        """Post handler"""
        # Preflight check to make sure volume exists
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        # If 'uploadId' Parameter is set, we should close the upload
        if 'uploadId' in request.GET:
            return self.post_handle_mp_complete(request, volumes.first(), path)
        return self.post_handle_mp_initiate(request, volumes.first(), path)

    def put(self, request, bucket, path):
        """PUT Handler"""
        # Preflight volume check
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        return self.put_handle_mp_part(request, volumes.first(), path)

    # pylint: disable=too-many-branches
    def post_handle_mp_complete(self, request, volume, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadComplete.html"""
        upload_id = request.GET.get('uploadId')
        # Ensure Multipart upload has started, otherwise 404
        get_list_for_user_or_404(request.user, 'p2_core.change_blob', **{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'volume': volume
        })

        def generator():
            """start task, generating spaces to keep connection alive"""
            yield '<?xml version="1.0" encoding="utf8"?>'  # Yield XML Header
            task = complete_multipart_upload.delay(
                upload_id=upload_id,
                user_pk=request.user.pk,
                volume_pk=volume.pk,
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
            'volume': volume
        })
        root = ElementTree.Element("{%s}InitiateMultipartUploadResult" % XML_NAMESPACE)
        ElementTree.SubElement(root, "Bucket").text = volume.name
        ElementTree.SubElement(root, "Key").text = path
        if existing.exists():
            blob = existing.first()
        else:
            blob = Blob.objects.create(
                path='/%s/%d' % (uuid4().hex, 1),
                volume=volume,
                tags={
                    TAG_S3_MULTIPART_BLOB_PART: 1,
                    TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
                    TAG_S3_MULTIPART_BLOB_UPLOAD_ID: uuid4().hex
                }
            )
        ElementTree.SubElement(root, "UploadId").text = blob.tags[TAG_S3_MULTIPART_BLOB_UPLOAD_ID]
        return XMLResponse(root)

    def put_handle_mp_part(self, request, volume, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadUploadPart.html"""
        upload_id = request.GET.get('uploadId')
        part_number = int(request.GET.get('partNumber'))
        # Ensure Multipart upload has started, otherwise 404
        get_list_for_user_or_404(request.user, 'p2_core.change_blob', **{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'volume': volume
        })
        # Create new Upload part, or reuse existing part and overwrite data
        parts = get_objects_for_user(request.user, 'p2_core.change_blob').filter(**{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_PART: part_number,
            'volume': volume
        })
        if parts.exists():
            blob = parts.first()
        else:
            blob = Blob.objects.create(
                path='/%s/%d' % (upload_id, part_number),
                volume=volume,
                tags={
                    TAG_S3_MULTIPART_BLOB_PART: part_number,
                    TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
                    TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id
                }
            )
            assign_perm('p2_core.change_blob', request.user, blob)
        blob.write(request.body)
        blob.save()
        # This response needs an ETag
        response = HttpResponse(status=200)
        response['ETag'] = blob.uuid.hex
        return response
