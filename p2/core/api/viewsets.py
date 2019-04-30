"""Core API Viewsets"""
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from p2.core.api.filters import BlobFilter
from p2.core.api.serializers import (BlobPayloadSerializer, BlobSerializer,
                                     StorageSerializer, VolumeSerializer)
from p2.core.models import Blob, Storage, Volume
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
        volumes = get_objects_for_user(request.user, 'p2_core.use_volume')
        if not volumes.exists():
            raise Http404
        volume = volumes.first()
        count = 0
        # TODO: Check blob create permissions
        for key in request.FILES:
            file = request.FILES[key]
            blob = Blob.objects.create(
                path=file.name,
                volume=volume,
                payload=file.read()
            )
            # assign permission to blob
            assign_perm('view_blob', request.user, blob)
            count += 1
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
