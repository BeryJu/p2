"""p2 s3 serializers"""

from rest_framework.serializers import HyperlinkedModelSerializer

from p2.s3.models import S3AccessKey


class S3AccessKeySerializer(HyperlinkedModelSerializer):
    """S3AccessKey Serializer"""

    class Meta:

        model = S3AccessKey
        fields = ['user', 'access_key', 'secret_key', 'name']
