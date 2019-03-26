"""p2 core serializers"""

from rest_framework.serializers import HyperlinkedModelSerializer

from p2.core.models import BaseStorage, Blob, LocalFileStorage, Volume


class BlobSerializer(HyperlinkedModelSerializer):
    """Blob Serializer"""

    class Meta:

        model = Blob
        fields = ['path', 'volume', 'tags', 'attributes']

class VolumeSerializer(HyperlinkedModelSerializer):
    """Volume Serializer"""

    class Meta:

        model = Volume
        fields = ['name', 'storage']


class BaseStorageSerializer(HyperlinkedModelSerializer):
    """BaseStorage Serializer"""

    class Meta:

        model = BaseStorage
        fields = '__all__'


class LocalFileStorageSerializer(HyperlinkedModelSerializer):
    """LocalFileStorage Serializer"""

    class Meta:

        model = LocalFileStorage
        fields = '__all__'
