"""p2 API Urls"""
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from p2.core.api.permissions import CustomObjectPermissions
from p2.core.api.viewsets import (BaseStorageViewSet, BlobViewSet,
                                  LocalFileStorageViewSet, VolumeViewSet)

INFO = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    INFO,
    public=True,
    permission_classes=(CustomObjectPermissions,),
)

ROUTER = DefaultRouter()
ROUTER.register('blob', BlobViewSet)
ROUTER.register('volume', VolumeViewSet)
ROUTER.register('storage/base', BaseStorageViewSet)
ROUTER.register('storage/localfile', LocalFileStorageViewSet)
# ROUTER.register('collections', CollectionViewSet)
# ROUTER.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(ROUTER.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),

]
