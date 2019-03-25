"""p2 core serializers"""

from rest_framework.serializers import HyperlinkedModelSerializer

from p2.core.models import Blob, Volume


class BlobSerializer(HyperlinkedModelSerializer):
    """Blob Serializer"""

    class Meta:

        model = Blob
        fields = ['path', 'volume', 'tags']

class VolumeSerializer(HyperlinkedModelSerializer):
    """Volume Serializer"""

    class Meta:

        model = Volume
        fields = ['name', 'storage']
