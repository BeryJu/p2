"""p2 Root URLs"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# from p2.core.urls import ur

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

urlpatterns = [
    # We need to mount the S3 URLs twice since some clients make requests to /s3 and some to /s3/
    path('s3/', include('p2.s3.urls')),
    path('s3', include('p2.s3.urls')),
    path('', include('p2.access.urls')),
    path('_/accounts/login/', auth_views.LoginView.as_view(), name='accounts-login'),
    path('_/accounts/logout/', auth_views.LogoutView.as_view(), name='accounts-logout'),
    path('_/core/', include('p2.core.urls')),
    path('_/admin/', admin.site.urls),
    path('_/api/', include('p2.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('_/__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
