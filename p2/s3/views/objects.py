"""p2 S3 Object views"""
from xml.etree import ElementTree

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.constants import (ATTR_BLOB_HASH_MD5, ATTR_BLOB_MIME,
                               ATTR_BLOB_SIZE_BYTES)
from p2.core.exceptions import BlobException
from p2.core.http import BlobResponse
from p2.core.models import Blob, Volume
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.s3.auth import S3Authentication
from p2.s3.constants import XML_NAMESPACE, ErrorCodes
from p2.s3.http import XMLResponse
from p2.s3.models import MultipartUpload, MultipartUploadPart


class ObjectView(S3Authentication):
    """Object related views"""

    def head(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectHEAD.html"""
        path = '/' + path
        blobs = get_objects_for_user(request.user, 'view_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        blob = blobs.first()
        response = HttpResponse(status=200)
        response['Content-Length'] = blob.attributes.get(ATTR_BLOB_SIZE_BYTES)
        response['Content-Type'] = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
        return response

    def get(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html"""
        path = '/' + path
        blobs = get_objects_for_user(request.user, 'view_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        blob = blobs.first()
        return BlobResponse(blob)

    # pylint: disable=too-many-branches
    def post_part_complete(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadComplete.html"""
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        volume = volumes.first()
        blobs = get_objects_for_user(request.user, 'change_blob', Blob).filter(
            path=path, volume=volume)
        mul = get_object_or_404(MultipartUpload,
                                upload_id=request.GET.get('uploadId'), volume=volume, blob_key=path)
        blob = None
        if not blobs.exists():
            blob = Blob.objects.create(
                path=path,
                volume=volume)
            # We're creating a new blob, hence assign all default permissions
            for permission in ['view_blob', 'change_blob', 'delete_blob']:
                assign_perm('p2_core.%s' % permission, request.user, blob)
        else:
            blob = blobs.first()
        try:
            parts = MultipartUploadPart.objects.filter(upload=mul).order_by('part')
            for part in parts:
                blob.write(part.temporary_file.read())
            blob.save()
            # Blob has been saved without errors, let's delete everything
            for part in parts:
                part.cleanup()
            mul.delete()
        except BlobException as exc:
            return XMLResponse(exc)
        root = ElementTree.Element("{%s}CompleteMultipartUploadResult" % XML_NAMESPACE)
        ElementTree.SubElement(root, "Location").text = "http://nope"
        ElementTree.SubElement(root, "Bucket").text = bucket
        ElementTree.SubElement(root, "Key").text = path
        ElementTree.SubElement(root, "ETag").text = blob.attributes.get(ATTR_BLOB_HASH_MD5)
        return XMLResponse(root)

    def post(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadInitiate.html"""
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        # If 'uploadId' Parameter is set, we should close the upload
        if 'uploadId' in request.GET:
            return self.post_part_complete(request, bucket, path)
        # Check if an existing Multipart Upload exists
        existing = MultipartUpload.objects.filter(volume=volumes.first(), blob_key=path)
        mul = None
        if existing.exists():
            mul = existing.first()
        else:
            mul = MultipartUpload.objects.create(
                volume=volumes.first(),
                blob_key=path)
        root = ElementTree.Element("{%s}InitiateMultipartUploadResult" % XML_NAMESPACE)
        ElementTree.SubElement(root, "Bucket").text = volumes.first().name
        ElementTree.SubElement(root, "Key").text = path
        ElementTree.SubElement(root, "UploadId").text = mul.upload_id.hex
        return XMLResponse(root)

    def put_part(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/mpUploadUploadPart.html"""
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        volume = volumes.first()
        upload_id = request.GET.get('uploadId')
        part_number = int(request.GET.get('partNumber'))
        # Ensure Multipart upload has started, otherwise 404
        mul = get_object_for_user_or_404(request.user, 'p2_s3.change_multipartupload',
                                         upload_id=upload_id, volume=volume, blob_key=path)
        # Create new Upload part, or reuse existing part and overwrite data
        parts = MultipartUploadPart.objects.filter(upload=mul, part=part_number)
        if parts.exists():
            part = parts.first()
        else:
            part = MultipartUploadPart.objects.create(
                upload=mul,
                part=part_number)
            assign_perm('p2_s3.change_multipartuploadpart', request.user, part)
        part.temporary_file.write(request.body)
        part.temporary_file.flush()
        # This response needs an ETag
        response = HttpResponse(status=200)
        response['ETag'] = part.uuid.hex
        return response

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
        # Check if part of a multipart upload
        if 'uploadId' in request.GET:
            return self.put_part(request, bucket, path)
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        volume = volumes.first()
        path = '/' + path
        blobs = get_objects_for_user(request.user, 'change_blob', Blob).filter(
            path=path, volume__name=bucket)
        try:
            if not blobs.exists():
                blob = Blob.objects.create(
                    path=path,
                    volume=volume)
                blob.write(request.body)
                blob.save()
                # We're creating a new blob, hence assign all default permissions
                for permission in ['view_blob', 'change_blob', 'delete_blob']:
                    assign_perm('p2_core.%s' % permission, request.user, blob)
            else:
                blob = blobs.first()
                blob.write(request.body)
                blob.save()
        except BlobException as exc:
            return XMLResponse(exc)
        return HttpResponse(status=200)

    def delete(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectDELETE.html"""
        blobs = get_objects_for_user(request.user, 'delete_blob', Blob).filter(
            path='/' + path, volume__name=bucket)
        if not blobs.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        blob = blobs.first()
        blob.delete()
        return HttpResponse(status=204)
