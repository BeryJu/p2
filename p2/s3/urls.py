"""p2 S3 URLs"""
from django.urls import path, register_converter

from p2.s3.converters import EverythingConverter, S3BucketConverter
from p2.s3.views import buckets, objects

register_converter(S3BucketConverter, 's3')
register_converter(EverythingConverter, 'everything')

app_name = 'p2_s3'

# These patterns are always available and don't require an AWS Header
urlpatterns = [
    path('<s3:bucket>/', buckets.BucketView.as_view(), name='bucket'),
    path('<s3:bucket>/<everything:path>', objects.ObjectView.as_view(), name='bucket-object'),
]
