"""p2 serve serializers"""

from rest_framework.serializers import HyperlinkedModelSerializer

from p2.serve.models import ServeRule


class ServeRuleSerializer(HyperlinkedModelSerializer):
    """ServeRule Serializer"""

    class Meta:

        model = ServeRule
        fields = ['name', 'tags', 'blob_query']
