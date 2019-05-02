"""p2 Root URLs"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from p2.ui.views.errors import ServerErrorView

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

handler500 = ServerErrorView.as_view()

urlpatterns = [
    # Some s3 requests don't have a trailing slash hence we need to accept both
    url(r'^s3(?P<redundant_slash>/?)', include('p2.s3.urls', namespace='p2_s3')),
    path('', include('p2.serve.urls', namespace='p2_serve')),
    path('_/core/', include('p2.core.urls')), # TODO: Migrate these urls to api
    path('_/admin/', admin.site.urls),
    path('_/api/', include('p2.api.urls', namespace='p2_api')),
    path('', RedirectView.as_view(pattern_name='p2_ui:index')),
    path('_/ui/', include('p2.ui.urls', namespace='p2_ui')),
    path('_/accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('_/debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
