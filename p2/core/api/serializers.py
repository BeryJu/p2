"""p2 core serializers"""
from rest_framework.serializers import ReadOnlyField, Serializer

from p2.api.serializers import TagModelSerializer
from p2.core.models import BaseStorage, Blob, Volume


class BlobSerializer(TagModelSerializer):
    """Blob Serializer"""

    class Meta:

        model = Blob
        fields = ['uuid', 'path', 'volume', 'tags', 'attributes', 'predefined_keys']


class BlobPayloadSerializer(Serializer):
    """Blob payload serializer"""

    payload = ReadOnlyField()

    def create(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()


class VolumeSerializer(TagModelSerializer):
    """Volume Serializer"""

    class Meta:

        model = Volume
        fields = ['uuid', 'name', 'storage', 'tags', 'predefined_keys']


class BaseStorageSerializer(TagModelSerializer):
    """BaseStorage Serializer"""

    provider = ReadOnlyField()

    class Meta:

        model = BaseStorage
        fields = ['uuid', 'name', 'tags', 'predefined_keys', 'provider']
