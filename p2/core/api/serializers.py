"""p2 core serializers"""
from rest_framework.serializers import ReadOnlyField

from p2.api.serializers import TagModelSerializer
from p2.core.models import BaseStorage, Blob, Volume


class BlobSerializer(TagModelSerializer):
    """Blob Serializer"""

    class Meta:

        model = Blob
        fields = ['path', 'volume', 'tags', 'attributes', 'predefined_keys']


class VolumeSerializer(TagModelSerializer):
    """Volume Serializer"""

    class Meta:

        model = Volume
        fields = ['name', 'storage', 'tags', 'predefined_keys']


class BaseStorageSerializer(TagModelSerializer):
    """BaseStorage Serializer"""

    provider = ReadOnlyField()

    class Meta:

        model = BaseStorage
        fields = ['name', 'tags', 'predefined_keys', 'provider']
