"""Core API Viewsets"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from p2.core.api.filters import BlobFilter
from p2.core.api.serializers import (BaseStorageSerializer,
                                     BlobPayloadSerializer, BlobSerializer,
                                     VolumeSerializer)
from p2.core.models import BaseStorage, Blob, Volume
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


class StorageViewSet(ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = BaseStorage.objects.all().select_subclasses()
    serializer_class = BaseStorageSerializer
