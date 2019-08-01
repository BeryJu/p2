"""p2 API Urls"""
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from p2.api.permissions import CustomObjectPermissions
from p2.api.viewsets import APIKeyViewSet, UserViewSet
from p2.core.api.viewsets import BlobViewSet, StorageViewSet, VolumeViewSet
from p2.serve.api.viewsets import ServeRuleViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

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
ROUTER.register('system/user', UserViewSet)
ROUTER.register('system/key', APIKeyViewSet)
ROUTER.register('tier0/policy', ServeRuleViewSet)

app_name = 'p2_api'
urlpatterns = [
    path('v1/', include(ROUTER.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('jwt/token/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
    path('jwt/verify/', verify_jwt_token),
    path('swagger/', SchemaView.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]
