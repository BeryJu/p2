"""p2 signals"""
import hashlib

from django.core.signals import Signal
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from structlog import get_logger

from p2.core import constants
from p2.core.models import Blob
from p2.lib.hash import chunked_hasher_multiple

LOGGER = get_logger()

BLOB_PAYLOAD_UPDATED = Signal(providing_args=['blob'])
BLOB_ACCESS = Signal(providing_args=['status_code', ''])
BLOB_PRE_SAVE = Signal(providing_args=['blob'])
BLOB_POST_SAVE = Signal(providing_args=['blob'])


@receiver(pre_save, sender=Blob)
# pylint: disable=unused-argument
def blob_pre_save(sender, instance, **kwargs):
    """Trigger BLOB_PRE_SAVE"""
    BLOB_PRE_SAVE.send(sender=sender, blob=instance)


@receiver(post_save, sender=Blob)
# pylint: disable=unused-argument
def blob_post_save(sender, instance, **kwargs):
    """Trigger BLOB_POST_SAVE"""
    BLOB_POST_SAVE.send(sender=sender, blob=instance)


@receiver(pre_delete, sender=Blob)
# pylint: disable=unused-argument
def blob_pre_delete(sender, instance, **kwargs):
    """Tell storage to delete blob"""
    # TODO: Move this to task
    instance.volume.storage.controller.delete(instance)


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def blob_payload_hash(sender, blob, **kwargs):
    """Add common hashes as attributes"""
    hashers = [
        hashlib.md5(),
        hashlib.sha1(),
        hashlib.sha256(),
        hashlib.sha384(),
        hashlib.sha512(),
    ]
    hashes = chunked_hasher_multiple(hashers, blob)
    for hash_name, hash_digest in hashes.items():
        attr_name = getattr(constants, 'ATTR_BLOB_HASH_%s' % hash_name.upper())
        if attr_name not in blob.attributes or blob.attributes[attr_name] != hash_digest:
            blob.attributes[attr_name] = hash_digest
            LOGGER.debug("Updated blob hash", hash_name=hash_name, blob=blob, digest=hash_digest)
    blob.save()
