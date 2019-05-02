"""p2 sentry integration"""
from logging import getLogger

LOGGER = getLogger(__name__)


def before_send(event, hint):
    """Check if error is database error, and ignore if so"""
    from django_redis.exceptions import ConnectionInterrupted
    from django.db import OperationalError
    from rest_framework.exceptions import APIException
    ignored_classes = (
        OperationalError,
        ConnectionInterrupted,
        APIException,
    )
    if 'exc_info' in hint:
        _exc_type, exc_value, _ = hint['exc_info']
        if isinstance(exc_value, ignored_classes):
            LOGGER.info("Supressing error %r", exc_value)
            return None
    return event
