"""UI URLS"""
from django.urls import path

from p2.ui.views import general
from p2.ui.views.api import key
from p2.ui.views.core import blob, component, storage, volume
from p2.ui.views.log import adaptor, record
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
    # Blob creation disabled for now
    # path('core/blob/create/',
    #      blob.BlobCreateView.as_view(), name='core-blob-create'),
    path('core/blob/<uuid:pk>/',
         blob.BlobDetailView.as_view(), name='core-blob-detail'),
    path('core/blob/<uuid:pk>/update/',
         blob.BlobUpdateView.as_view(), name='core-blob-update'),
    path('core/blob/<uuid:pk>/delete/',
         blob.BlobDeleteView.as_view(), name='core-blob-delete'),
    path('core/blob/<uuid:pk>/download/',
         blob.BlobDownloadView.as_view(), name='core-blob-download'),
    # Core - Components
    path('core/volume/<uuid:pk>/component/create/',
         component.ComponentCreateView.as_view(), name='core-component-create'),
    path('core/component/<uuid:pk>/update/',
         component.ComponentUpdateView.as_view(), name='core-component-update'),
    path('core/component/<uuid:pk>/delete/',
         component.ComponentDeleteView.as_view(), name='core-component-delete'),
    # Core - Storages
    path('core/storage/',
         storage.StorageListView.as_view(), name='core-storage-list'),
    path('core/storage/create/',
         storage.StorageCreateView.as_view(), name='core-storage-create'),
    path('core/storage/<uuid:pk>/',
         storage.StorageDetailView.as_view(), name='core-storage-detail'),
    path('core/storage/<uuid:pk>/update/',
         storage.StorageUpdateView.as_view(), name='core-storage-update'),
    path('core/storage/<uuid:pk>/delete/',
         storage.StorageDeleteView.as_view(), name='core-storage-delete'),
    # API - Keys
    path('s3/access-key/',
         key.APIKeyListView.as_view(), name='api-key-list'),
    path('s3/access-key/create/',
         key.APIKeyCreateView.as_view(), name='api-key-create'),
    path('s3/access-key/<int:pk>/update/',
         key.APIKeyUpdateView.as_view(), name='api-key-update'),
    path('s3/access-key/<int:pk>/delete/',
         key.APIKeyDeleteView.as_view(), name='api-key-delete'),
    # Serve - Rules
    path('serve/rule/',
         rule.ServeRuleListView.as_view(), name='serve-rule-list'),
    path('serve/rule/create/',
         rule.ServeRuleCreateView.as_view(), name='serve-rule-create'),
    path('serve/rule/<uuid:pk>/debug/',
         rule.ServeRuleDebugView.as_view(), name='serve-rule-debug'),
    path('serve/rule/<uuid:pk>/update/',
         rule.ServeRuleUpdateView.as_view(), name='serve-rule-update'),
    path('serve/rule/<uuid:pk>/delete/',
         rule.ServeRuleDeleteView.as_view(), name='serve-rule-delete'),
]
