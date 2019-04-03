"""Core API Viewsets"""
from rest_framework import viewsets

from p2.core.api.filters import BlobFilter
from p2.core.api.serializers import (BaseStorageSerializer, BlobSerializer,
                                     VolumeSerializer)
from p2.core.models import BaseStorage, Blob, Volume


class BlobViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = Blob.objects.all()
    serializer_class = BlobSerializer
    filter_class = BlobFilter


class VolumeViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer


class StorageViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = BaseStorage.objects.all().select_subclasses()
    serializer_class = BaseStorageSerializer
