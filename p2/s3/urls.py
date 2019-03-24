
# from django.urls import url
from django.conf.urls import url
from django.urls import path, register_converter

from p2.s3.converters import PathConverter, S3BucketConverter
from p2.s3.views import buckets, debug, get, objects

register_converter(S3BucketConverter, 's3')
register_converter(PathConverter, 'path')

urlpatterns = [
    path('<s3:bucket>', buckets.BucketView.as_view(), name='bucket'),
    path('<s3:bucket>/', buckets.BucketView.as_view(), name='bucket'),
    path('<s3:bucket>/<path:path>', objects.ObjectView.as_view(), name='bucket'),
    path('', get.ListView.as_view(), name='list'),
    # url(r'.*', debug.DebugView.as_view(), name='debug')
]
