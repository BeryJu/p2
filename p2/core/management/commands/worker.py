"""p2 Worker management command"""

from django.core.management.base import BaseCommand
from structlog import get_logger

from p2.core.celery import CELERY_APP

LOGGER = get_logger()


class Command(BaseCommand):
    """Run Celery Worker"""

    def handle(self, *args, **options):
        """celery worker"""
        CELERY_APP.worker_main(['worker', '--autoscale=10,3', '-E', '-B'])
