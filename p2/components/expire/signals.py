"""expire signals (schedule expiry when blob metadata is saved)"""
from datetime import datetime

from django.dispatch import receiver
from django.utils.timezone import make_aware
from pytz.exceptions import InvalidTimeError
from structlog import get_logger

from p2.components.expire.constants import TAG_EXPIRE_DATE
from p2.components.expire.tasks import run_expire
from p2.core.signals import BLOB_POST_SAVE

LOGGER = get_logger()

@receiver(BLOB_POST_SAVE)
# pylint: disable=unused-argument
def blob_post_save_expire(blob, *args, **kwargs):
    """Schedule blob deletion on metadata save"""
    if TAG_EXPIRE_DATE in blob.tags:
        try:
            date = make_aware(datetime.fromtimestamp(blob.tags.get(TAG_EXPIRE_DATE)))
        except InvalidTimeError:
            # We couldn't convert time, assume invalid value
            return
        run_expire.apply_async(eta=date)
        LOGGER.debug("Scheduled blob for deletion", blob=blob, at=date)
