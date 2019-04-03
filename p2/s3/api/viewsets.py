"""s3 API Viewsets"""
from rest_framework import viewsets

from p2.s3.api.serializers import S3AccessKeySerializer
from p2.s3.models import S3AccessKey


class S3AccessKeyViewSet(viewsets.ModelViewSet):
    """
    Viewset that only lists events if user has 'view' permissions, and only
    allows operations on individual events if user has appropriate 'view', 'add',
    'change' or 'delete' permissions.
    """
    queryset = S3AccessKey.objects.all()
    serializer_class = S3AccessKeySerializer
