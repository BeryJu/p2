"""UI URLS"""
from django.urls import path

from p2.ui.views import general
from p2.ui.views.core import blob, volume
from p2.ui.views.log import records
from p2.ui.views.s3 import access_key

app_name = 'p2_ui'
urlpatterns = [
    # General
    path('', general.IndexView.as_view(), name='index'),
    # Core - Volumes
    path('core/volume/',
         volume.VolumeListView.as_view(), name='core-volume-list'),
    path('core/volume/create/',
         volume.VolumeCreateView.as_view(), name='core-volume-create'),
    path('core/volume/<uuid:pk>/update/',
         volume.VolumeUpdateView.as_view(), name='core-volume-update'),
    path('core/volume/<uuid:pk>/delete/',
         volume.VolumeDeleteView.as_view(), name='core-volume-delete'),
    path('core/volume/<uuid:pk>/blobs/',
         blob.BlobListView.as_view(), name='core-blob-list'),
    # Core - Blobs
    path('core/blobs/create/',
         blob.BlobCreateView.as_view(), name='core-blob-create'),
    path('core/blobs/<uuid:pk>/update/',
         blob.BlobUpdateView.as_view(), name='core-blob-update'),
    path('core/blobs/<uuid:pk>/delete/',
         blob.BlobDeleteView.as_view(), name='core-blob-delete'),
    path('core/blobs/<uuid:pk>/download/',
         blob.BlobDownloadView.as_view(), name='core-blob-download'),
    # S3
    path('s3/access-key/',
         access_key.S3AccessKeyListView.as_view(), name='s3-access-key-list'),
    path('s3/access-key/create/',
         access_key.S3AccessKeyCreateView.as_view(), name='s3-access-key-create'),
    path('s3/access-key/<int:pk>/update/',
         access_key.S3AccessKeyUpdateView.as_view(), name='s3-access-key-update'),
    path('s3/access-key/<int:pk>/delete/',
         access_key.S3AccessKeyDeleteView.as_view(), name='s3-access-key-delete'),
    # Log
    path('log/adaptor/<uuid:pk>/records/',
         records.RecordListView.as_view(), name='log-records-list'),
]
