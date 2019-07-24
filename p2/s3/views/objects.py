"""p2 S3 Object views"""
from django.http.response import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.constants import ATTR_BLOB_MIME, ATTR_BLOB_SIZE_BYTES
from p2.core.exceptions import BlobException
from p2.core.http import BlobResponse
from p2.core.models import Blob, Volume
from p2.s3.errors import AWSNoSuchKey, AWSNotImplemented
from p2.s3.http import XMLResponse
from p2.s3.views.multipart import MultipartUploadView


class ObjectView(View):
    """Object related views"""

    volume = None

    @csrf_exempt
    def dispatch(self, request, bucket, path):
        """Preflight checks, lookup volume, etc"""
        # Preflight volume check - Check for use_volume permission is POST & PUT, otherwise
        # we don't care about volume permission here
        if request.method in ['POST', 'PUT']:
            volumes = get_objects_for_user(request.user, 'p2_core.use_volume').filter(name=bucket)
        else:
            volumes = Volume.objects.filter(name=bucket)
        if not volumes.exists():
            raise AWSNoSuchKey
        self.volume = volumes.first()
        # Make sure path is prefixed with /
        if not path.startswith('/'):
            path = '/' + path
        return super().dispatch(request, bucket, path)

    ## HTTP Method handlers

    def head(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectHEAD.html"""
        blobs = get_objects_for_user(request.user, 'view_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            raise AWSNoSuchKey
        blob = blobs.first()
        # We're not using BlobResponse here since we only want the attributes
        response = HttpResponse(status=200)
        response['Content-Length'] = blob.attributes.get(ATTR_BLOB_SIZE_BYTES)
        response['Content-Type'] = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
        return response

    def get(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html"""
        blobs = get_objects_for_user(request.user, 'view_blob', Blob).filter(
            path=path, volume__name=bucket)
        if not blobs.exists():
            raise AWSNoSuchKey
        blob = blobs.first()
        return BlobResponse(blob)

    def post(self, request, bucket, path):
        """Post handler"""
        if 'select-type' in request.GET:
            return self.select(request, bucket, path)
        # POST is handled by the MultipartUploadView
        return MultipartUploadView().dispatch(request, bucket, path)

    def select(self, request, bucket, path):
        """S3Select"""
        raise AWSNotImplemented

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
        # Check if part of a multipart upload
        if 'uploadId' in request.GET:
            return MultipartUploadView().dispatch(request, bucket, path)
        blobs = get_objects_for_user(request.user, 'p2_core.change_blob').filter(
            path=path, volume__name=bucket)
        try:
            if not blobs.exists() and request.user.has_perm('p2_core.add_blob'):
                blob = Blob.objects.create(
                    path=path,
                    volume=self.volume)
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
            path=path, volume__name=bucket)
        if not blobs.exists():
            raise AWSNoSuchKey
        blob = blobs.first()
        blob.delete()
        return HttpResponse(status=204)
