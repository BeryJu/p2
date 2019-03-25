"""p2 Root URLs"""
from django.contrib import admin
from django.urls import include, path

# from p2.core.urls import ur

admin.site.index_title = 'p2 Admin'
admin.site.site_title = 'p2'

urlpatterns = [
    path('', include('p2.access.urls')),
    path('core/', include('p2.core.urls')),
    path('s3/', include('p2.s3.urls')),
    path('admin/', admin.site.urls),
]
