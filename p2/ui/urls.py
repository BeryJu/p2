"""UI URLS"""
from django.urls import path

from p2.ui.views import general
from p2.ui.views.core import blob, storage, volume
from p2.ui.views.log import record
from p2.ui.views.s3 import access_key
from p2.ui.views.serve import rule

app_name = 'p2_ui'
urlpatterns = [
    # General
    path('', general.IndexView.as_view(), name='index'),
    # Core - Volumes
    path('core/volume/',
         volume.VolumeListView.as_view(), name='core-volume-list'),
    path('core/volume/create/',
         volume.VolumeCreateView.as_view(), name='core-volume-create'),
    path('core/volume/<uuid:pk>/',
         volume.VolumeDetailView.as_view(), name='core-volume-detail'),
    path('core/volume/<uuid:pk>/update/',
         volume.VolumeUpdateView.as_view(), name='core-volume-update'),
    path('core/volume/<uuid:pk>/delete/',
         volume.VolumeDeleteView.as_view(), name='core-volume-delete'),
    path('core/volume/<uuid:pk>/blobs/',
         blob.FileBrowserView.as_view(), name='core-blob-list'),
    # Core - Blobs
    path('core/blobs/create/',
         blob.BlobCreateView.as_view(), name='core-blob-create'),
    path('core/blobs/<uuid:pk>/update/',
         blob.BlobUpdateView.as_view(), name='core-blob-update'),
    path('core/blobs/<uuid:pk>/delete/',
         blob.BlobDeleteView.as_view(), name='core-blob-delete'),
    path('core/blobs/<uuid:pk>/download/',
         blob.BlobDownloadView.as_view(), name='core-blob-download'),
    # Core - Storages
    path('core/storage/',
         storage.StorageListView.as_view(), name='core-storage-list'),
    path('core/storage/create/',
         storage.StorageCreateView.as_view(), name='core-storage-create'),
    path('core/storage/<uuid:pk>/update/',
         storage.StorageUpdateView.as_view(), name='core-storage-update'),
    path('core/storage/<uuid:pk>/delete/',
         storage.StorageDeleteView.as_view(), name='core-storage-delete'),
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
         record.RecordListView.as_view(), name='log-records-list'),
    # Serve - Rules
    path('serve/rule/',
         rule.ServeRuleListView.as_view(), name='serve-rule-list'),
    path('serve/rule/create/',
         rule.ServeRuleCreateView.as_view(), name='serve-rule-create'),
    path('serve/rule/<int:pk>/update/',
         rule.ServeRuleUpdateView.as_view(), name='serve-rule-update'),
    path('serve/rule/<int:pk>/delete/',
         rule.ServeRuleDeleteView.as_view(), name='serve-rule-delete'),
]
