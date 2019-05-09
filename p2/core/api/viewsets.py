"""Core API Viewsets"""
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import assign_perm
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from p2.core.api.filters import BlobFilter
from p2.core.api.serializers import (BlobPayloadSerializer, BlobSerializer,
                                     StorageSerializer, VolumeSerializer)
from p2.core.exceptions import BlobException
from p2.core.models import Blob, Storage, Volume
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.lib.utils import b64encode


class BlobViewSet(ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = Blob.objects.all()
    serializer_class = BlobSerializer
    filter_class = BlobFilter

    @swagger_auto_schema(method='GET', responses={
        '200': BlobPayloadSerializer()
    })
    @action(detail=True, methods=['get'])
    # pylint: disable=invalid-name
    def payload(self, request, pk=None):
        """Return payload data as base64 string"""
        blob = self.get_object()
        return Response({
            'payload': 'data:%s;base64,%s' % (blob.attributes.get('mime', 'text/plain'),
                                              b64encode(blob.payload).decode('utf-8'))
        })

class VolumeViewSet(ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer

    # @swagger_auto_schema(method='POST', responses={
    #     '200': BlobPayloadSerializer()
    # })
    @action(detail=True, methods=['post'])
    # pylint: disable=invalid-name
    def upload(self, request, pk=None):
        """Create blob from HTML Form upload"""
        volume = get_object_for_user_or_404(request.user, 'p2_core.use_volume', pk=pk)
        count = 0
        if not request.user.has_perm('p2_core.create_blob'):
            raise PermissionDenied()
        # If upload was made from a subdirectory, we accept the ?prefix parameter
        prefix = request.GET.get('prefix', '')
        for key in request.FILES:
            file = request.FILES[key]
            try:
                blob = Blob.from_uploaded_file(file, volume, prefix=prefix)
                # assign permission to blob
                for permission in ['view_blob', 'update_blob', 'delete_blob']:
                    assign_perm('p2_core.%s' % permission, request.user, blob)
                count += 1
            except BlobException as exc:
                raise APIException(detail=repr(exc))
        return Response({
            'count': count
        })

class StorageViewSet(ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
