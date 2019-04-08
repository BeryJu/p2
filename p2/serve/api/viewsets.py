"""serve API Viewsets"""
from rest_framework import viewsets

from p2.serve.api.serializers import ServeRuleSerializer
from p2.serve.models import ServeRule


class ServeRuleViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = ServeRule.objects.all()
    serializer_class = ServeRuleSerializer
