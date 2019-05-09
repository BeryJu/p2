"""API Viewsets"""
from django.contrib.auth.models import User
from rest_framework import viewsets

from p2.api.models import APIKey
from p2.api.serializers import APIKeySerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
