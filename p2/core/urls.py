"""p2 URL Configuration"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path
from django.views.generic.base import RedirectView

# from p2.api.urls import urlpatterns as api_urlpatterns
# from p2.core.views import clients, core, upload, view
# from p2.core.views import upload

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

urlpatterns = [
    # path('', RedirectView.as_view(url='overview/')),
    # path('api/', include(api_urlpatterns)),
    # path('overview/', core.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    # path('accounts/allauth/', include('allauth.urls')),
    path('accounts/login/', views.LoginView.as_view(), name='accounts-login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='accounts-logout'),
    # Legacy upload URL
    # path('gyazo.php', upload.LegacyObjectView.as_view(), name='upload'),
    # path('upload/', upload.LegacyObjectView.as_view(), name='upload'),
    # All view URLs are handeled by the same Function, but we need different names
    # so the default can be changed in the settings
    # url(r'^(?P<file_hash>\w{16})(\..{1,5})?$',
    #     view.ObjectViewFile.as_view(), name='view_sha512_short'),
    # url(r'^(?P<file_hash>\w{32})(\..{1,5})?$',
    #     view.ObjectViewFile.as_view(), name='view_md5'),
    # url(r'^(?P<file_hash>\w{64})(\..{1,5})?$',
    #     view.ObjectViewFile.as_view(), name='view_sha256'),
    # url(r'^(?P<file_hash>\w{128})(\..{1,5})?$',
    #     view.ObjectViewFile.as_view(), name='view_sha512'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
