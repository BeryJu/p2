"""p2 access serializers"""

from rest_framework.serializers import HyperlinkedModelSerializer

from p2.access.models import AccessRule


class AccessRuleSerializer(HyperlinkedModelSerializer):
    """AccessRule Serializer"""

    class Meta:

        model = AccessRule
        fields = ['match', 'blob_query']
