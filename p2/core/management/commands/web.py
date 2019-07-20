"""p2 Tornado management command"""

from logging import getLogger
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from django.core.management.base import BaseCommand
from django.utils import autoreload
from django.core.wsgi import get_wsgi_application

LOGGER = getLogger(__name__)


class Command(BaseCommand):
    """Run Tornado Server"""

    def handle(self, *args, **options):
        """Start Tornado server"""
        container = WSGIContainer(get_wsgi_application())
        http_server = HTTPServer(container)
        http_server.listen(8000, '0.0.0.0')
        IOLoop.current().start()
