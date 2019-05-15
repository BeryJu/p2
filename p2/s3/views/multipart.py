"""p2 S3 Object views"""
from uuid import uuid4
from xml.etree import ElementTree

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.http.response import HttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.constants import ATTR_BLOB_HASH_MD5
from p2.core.exceptions import BlobException
from p2.core.models import Blob, Volume
from p2.lib.shortcuts import get_list_for_user_or_404
from p2.s3.auth import S3Authentication
from p2.s3.constants import (TAG_S3_MULTIPART_BLOB_PART,
                             TAG_S3_MULTIPART_BLOB_TARGET_BLOB,
                             TAG_S3_MULTIPART_BLOB_UPLOAD_ID, XML_NAMESPACE,
                             ErrorCodes)
from p2.s3.http import XMLResponse


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
        # Create the destination blob
        blobs = get_objects_for_user(request.user, 'p2_core.change_blob', Blob).filter(
            path=path, volume=volume)
        if not blobs.exists():
            destination_blob = Blob.objects.create(
                path=path,
                volume=volume)
            # We're creating a new blob, hence assign all default permissions
            for permission in ['view_blob', 'change_blob', 'delete_blob']:
                assign_perm('p2_core.%s' % permission, request.user, destination_blob)
        else:
            destination_blob = blobs.first()
        # Go through all temporary blobs and combine them into one
        try:
            parts = get_objects_for_user(request.user, 'p2_core.change_blob').filter(**{
                'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
                'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
            })
            # We need to annotate TAG_S3_MULTIPART_BLOB_PART so we can use order_by
            parts = parts.annotate(part_number=KeyTextTransform(TAG_S3_MULTIPART_BLOB_PART, 'tags'))
            parts = parts.order_by('part_number')
            for part in parts:
                destination_blob.write(part.read())
            destination_blob.save()
            parts.delete()
        except BlobException as exc:
            return XMLResponse(exc)
        root = ElementTree.Element("{%s}CompleteMultipartUploadResult" % XML_NAMESPACE)
        ElementTree.SubElement(root, "Location").text = "http://nope"
        ElementTree.SubElement(root, "Bucket").text = volume.name
        ElementTree.SubElement(root, "Key").text = path
        ElementTree.SubElement(root, "ETag").text = \
            destination_blob.attributes.get(ATTR_BLOB_HASH_MD5)
        return XMLResponse(root)

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
                path='/%s' % uuid4().hex,
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

        # parts = MultipartUploadPart.objects.filter(
        #     upload=mul, part=part_number)
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
