"""p2 S3 Object views"""
from django.http.response import HttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user
from structlog import get_logger

from p2.core.constants import (ATTR_BLOB_IS_FOLDER, ATTR_BLOB_MIME,
                               ATTR_BLOB_SIZE_BYTES)
from p2.core.http import BlobResponse
from p2.core.models import Blob, Volume
from p2.core.prefix_helper import make_absolute_path, make_absolute_prefix
from p2.s3.errors import AWSAccessDenied, AWSNoSuchBucket, AWSNoSuchKey
from p2.s3.views.common import S3View
from p2.s3.views.multipart import MultipartUploadView

LOGGER = get_logger()


class ObjectView(S3View):
    """Object related views"""

    volume = None

    def dispatch(self, request, bucket, path):
        """Preflight checks, lookup volume, etc"""
        # Preflight volume check - Check for use_volume permission is POST & PUT, otherwise
        # we don't care about volume permission here
        if request.method in ['POST', 'PUT']:
            volumes = get_objects_for_user(request.user, 'p2_core.use_volume').filter(name=bucket)
        else:
            volumes = Volume.objects.filter(name=bucket)
        if not volumes.exists():
            raise AWSNoSuchBucket
        self.volume = volumes.first()
        # Make sure path is prefixed with /
        # If path ends with /, a path to a folder has been given
        if path.endswith('/'):
            path = make_absolute_prefix(path)
        else:
            path = make_absolute_path(path)
        return super().dispatch(request, bucket, path)

    ## HTTP Method handlers

    def head(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectHEAD.html"""
        blob = self.get_blob('view_blob', path=path, volume__name=bucket)
        # We're not using BlobResponse here since we only want the attributes
        response = HttpResponse(status=200)
        response['Content-Length'] = blob.attributes.get(ATTR_BLOB_SIZE_BYTES)
        response['Content-Type'] = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
        return response

    def get(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html"""
        blob = self.get_blob('view_blob', path=path, volume__name=bucket)
        return BlobResponse(blob)

    def post(self, request, bucket, path):
        """Post handler"""
        # POST is handled by the MultipartUploadView
        return MultipartUploadView().dispatch(request, bucket, path)

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
        # Check if part of a multipart upload
        if 'uploadId' in request.GET:
            return MultipartUploadView().dispatch(request, bucket, path)
        try:
            blob = self.get_blob('change_blob', path=path, volume=self.volume)
            blob.write(request.body)
            blob.save()
        except AWSNoSuchKey:
            if not request.user.has_perm('p2_core.add_blob'):
                raise AWSAccessDenied
            # Blob doesn't exist, user can create
            blob = Blob.objects.create(
                path=path,
                volume=self.volume)
            # Check if request.body is empty to correctly create folders
            if request.body == b'':
                blob.attributes[ATTR_BLOB_IS_FOLDER] = True
            blob.write(request.body)
            blob.save()
            for permission in ['view_blob', 'change_blob', 'delete_blob']:
                assign_perm('p2_core.%s' % permission, request.user, blob)
        return HttpResponse(status=200)

    def delete(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectDELETE.html"""
        blob = self.get_blob('delete_blob', path=path, volume__name=bucket)
        blob.delete()
        return HttpResponse(status=204)
