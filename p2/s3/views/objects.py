"""p2 S3 Object views"""
from django.http.response import HttpResponse
from guardian.shortcuts import get_objects_for_user

from p2.core.constants import ATTR_BLOB_MINE, ATTR_BLOB_SIZE_BYTES
from p2.core.models import Blob, Volume
from p2.s3.auth import S3Authentication
from p2.s3.constants import ErrorCodes


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
        response['Content-Type'] = blob.attributes.get(ATTR_BLOB_MINE, 'text/plain')
        return response

    def get(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html"""
        path = '/' + path
        blobs = get_objects_for_user(request.user, 'view_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        blob = blobs.first()
        response = HttpResponse(blob.payload)
        response['Content-Length'] = blob.attributes.get(ATTR_BLOB_SIZE_BYTES)
        response['Content-Type'] = blob.attributes.get(ATTR_BLOB_MINE, 'text/plain')
        return response

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
        volumes = get_objects_for_user(request.user, 'use_volume', Volume).filter(name=bucket)
        if not volumes.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        volume = volumes.first()
        path = '/' + path
        blobs = get_objects_for_user(request.user, 'change_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            blob = Blob(path=path, volume=volume)
        else:
            blob = blobs.first()
        blob.payload = request.body
        blob.save()
        return HttpResponse(status=200)

    def delete(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectDELETE.html"""
        blobs = get_objects_for_user(request.user, 'delete_blob', Blob).filter(
            path='/' + path, volume__name=bucket)
        if not blobs.exists():
            return self.error_response(ErrorCodes.NO_SUCH_KEY)
        blob = blobs.first()
        blob.delete()
        response = HttpResponse(status=204)
        return response
