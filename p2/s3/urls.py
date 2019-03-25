"""p2 S3 URLs"""
from django.urls import path, register_converter

from p2.s3.converters import EverythingConverter, S3BucketConverter
from p2.s3.views import buckets, get, objects

register_converter(S3BucketConverter, 's3')
register_converter(EverythingConverter, 'everything')

urlpatterns = [
    path('<s3:bucket>', buckets.BucketView.as_view(), name='bucket'),
    path('<s3:bucket>/', buckets.BucketView.as_view(), name='bucket'),
    path('<s3:bucket>/<everything:path>', objects.ObjectView.as_view(), name='bucket'),
    path('', get.ListView.as_view(), name='list'),
    # url(r'.*', debug.DebugView.as_view(), name='debug')
]
