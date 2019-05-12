"""p2 S3 Object views"""
from django.http.response import HttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.constants import ATTR_BLOB_MIME, ATTR_BLOB_SIZE_BYTES
from p2.core.exceptions import BlobException
from p2.core.http import BlobResponse
from p2.core.models import Blob, Volume
from p2.s3.auth import S3Authentication
from p2.s3.constants import ErrorCodes
from p2.s3.http import XMLResponse


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

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
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
                # TODO: Implement chunked saving
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
