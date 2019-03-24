from rest_framework.serializers import HyperlinkedModelSerializer

from p2.core.models import Blob, Volume


class BlobSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Blob
        fields = ['path', 'volume', 'tags']

class VolumeSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Volume
        fields = ['name', 'storage']
