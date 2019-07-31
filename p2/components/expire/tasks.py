"""expiry tasks"""
from structlog import get_logger

from p2.components.expire.controller import ExpiryController
from p2.core.celery import CELERY_APP
from p2.core.models import Component
from p2.lib.reflection import class_to_path

LOGGER = get_logger()

@CELERY_APP.task(bind=True)
# pylint: disable=unused-argument
def run_expire(self):
    """Remove blobs which have expired"""
    LOGGER.debug("Running expiry...")
    for component in Component.objects.filter(
            controller_path=class_to_path(ExpiryController),
            enabled=True):
        component.controller.expire_volume(component.volume)

@CELERY_APP.on_after_configure.connect
# pylint: disable=unused-argument
def setup_periodic_tasks(sender, **kwargs):
    """Run expiry task every 60 seconds"""
    sender.add_periodic_task(60.0, run_expire.s())
