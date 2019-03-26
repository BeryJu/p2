"""p2 API Urls"""
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from p2.core.api.viewsets import (BaseStorageViewSet, BlobViewSet,
                                  LocalFileStorageViewSet, VolumeViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

ROUTER = DefaultRouter()
ROUTER.register('blobs', BlobViewSet)
ROUTER.register('volumes', VolumeViewSet)
ROUTER.register('storage/base', BaseStorageViewSet)
ROUTER.register('storage/localfile', LocalFileStorageViewSet)
# ROUTER.register('collections', CollectionViewSet)
# ROUTER.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(ROUTER.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

]
