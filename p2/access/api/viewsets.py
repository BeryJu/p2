"""access API Viewsets"""
from rest_framework import viewsets

from p2.access.api.serializers import AccessRuleSerializer
from p2.access.models import AccessRule


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
