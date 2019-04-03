"""p2 URL Configuration"""
from django.urls import path

from p2.core.views import upload

urlpatterns = [
    # Legacy upload URL
    path('gyazo.php', upload.LegacyObjectView.as_view(), name='upload'),
    path('upload/', upload.LegacyObjectView.as_view(), name='upload'),
]
