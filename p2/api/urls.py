"""p2 API Urls"""
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from p2.access.api.viewsets import AccessRuleViewSet
from p2.api.permissions import CustomObjectPermissions
from p2.api.viewsets import UserViewSet
from p2.core.api.viewsets import BlobViewSet, StorageViewSet, VolumeViewSet
from p2.s3.api.viewsets import S3AccessKeyViewSet

INFO = openapi.Info(
    title="p2 API",
    default_version='v1',
    description="p2 API",
    contact=openapi.Contact(email="hello@beryju.org"),
    license=openapi.License(name="MIT License"),
)

SchemaView = get_schema_view(
    INFO,
    public=True,
    permission_classes=(CustomObjectPermissions,),
)

ROUTER = DefaultRouter()
ROUTER.register('core/blob', BlobViewSet)
ROUTER.register('core/volume', VolumeViewSet)
ROUTER.register('core/storage', StorageViewSet)
ROUTER.register('core/user', UserViewSet)
ROUTER.register('s3/access_key', S3AccessKeyViewSet)
ROUTER.register('access/rule', AccessRuleViewSet)

urlpatterns = [
    path('v1/', include(ROUTER.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]
