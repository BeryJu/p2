"""p2 k8s api views"""
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from p2.k8s.component_controller import (GRPC_DEPLOYMENT, STATIC_DEPLOYMENT,
                                         TIER0_DEPLOYMENT, WEB_DEPLOYMENT,
                                         WORKER_DEPLOYMENT)

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
        """Return a list of all manageable components"""
        return Response(CONTROLLER_MAP.keys())

    # pylint: disable=invalid-name
    def retrieve(self, request, pk):
        """Return the current scale of the given component"""
        return Response(CONTROLLER_MAP[pk].scale)
