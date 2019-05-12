"""p2 Root URLs"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from p2.lib.config import CONFIG
from p2.ui.views.errors import ServerErrorView

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

handler500 = ServerErrorView.as_view()

# S3 URLs get routed via middleware
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='p2_ui:index')),
    path('_/admin/', admin.site.urls),
    path('_/api/', include('p2.api.urls', namespace='p2_api')),
    path('_/ui/', include('p2.ui.urls', namespace='p2_ui')),
    path('_/accounts/', include('allauth.urls')),
    path('', include('p2.s3.urls', namespace='p2_s3')),
    path('', include('p2.serve.urls', namespace='p2_serve')),
]

if CONFIG.get('legacy_upload_enabled'):
    from p2.api.legacy import LegacyObjectView
    urlpatterns = [
        # Legacy upload URL
        path('gyazo.php', LegacyObjectView.as_view(), name='upload'),
        path('upload/', LegacyObjectView.as_view(), name='upload'),
    ] + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('_/debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
