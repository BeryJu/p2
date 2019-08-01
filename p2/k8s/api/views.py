"""p2 k8s api views"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from p2.k8s.component_controller import WEB_DEPLOYMENT, GRPC_DEPLOYMENT, STATIC_DEPLOYMENT, TIER0_DEPLOYMENT, WORKER_DEPLOYMENT
from rest_framework.permissions import IsAdminUser

CONTROLLER_MAP = {
    'web': WEB_DEPLOYMENT,
    'grpc': GRPC_DEPLOYMENT,
    'static': STATIC_DEPLOYMENT,
    'tier0': TIER0_DEPLOYMENT,
    'worker': WORKER_DEPLOYMENT
}


class ScaleAPIViewSet(ViewSet):
    """Scale various features of p2 Up and Down as well as controlling AutoScaling."""
    permission_classes = [IsAdminUser]

    def list(self, request):
        return Response(CONTROLLER_MAP.keys())

    def retrieve(self, request, pk):
        return Response(CONTROLLER_MAP[pk].scale)

    def update(self, request, pk, **kwargs):
        print(kwargs)
