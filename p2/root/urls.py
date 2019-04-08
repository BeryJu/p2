"""p2 Root URLs"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

# from p2.core.urls import ur

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

urlpatterns = [
    # We need to mount the S3 URLs twice since some clients make requests to /s3 and some to /s3/
    path('s3/', include('p2.s3.urls')),
    path('s3', include('p2.s3.urls')),
    path('', include('p2.serve.urls')),
    path('_/core/', include('p2.core.urls')),
    path('_/admin/', admin.site.urls),
    path('_/api/', include('p2.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('_/__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
