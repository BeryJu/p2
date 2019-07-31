"""p2 GRPC management command"""

import time
from concurrent import futures
from contextlib import contextmanager

import grpc
from django.core.management.base import BaseCommand
from django.utils import autoreload
from grpc_reflection.v1alpha import reflection
from prometheus_client import start_http_server
from py_grpc_prometheus.prometheus_server_interceptor import \
    PromServerInterceptor
from structlog import get_logger

from p2.grpc.protos import serve_pb2, serve_pb2_grpc
from p2.serve.grpc import Serve

LOGGER = get_logger()
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


@contextmanager
def serve_forever():
    """Run GRPC server, blocking"""
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10), interceptors=(PromServerInterceptor(),))
    serve_pb2_grpc.add_ServeServicer_to_server(Serve(), server)
    service_names = (
        serve_pb2.DESCRIPTOR.services_by_name['Serve'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    LOGGER.debug('Successfully started grpc server on port 50051')

    # Start an end point to expose metrics.
    LOGGER.debug("Prometheus Server running on port 9102")
    start_http_server(9102)
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)

class Command(BaseCommand):
    """Run GRPC Server"""

    def handle(self, *args, **options):
        """Start GRPC server and register services"""
        autoreload.run_with_reloader(serve_forever)
