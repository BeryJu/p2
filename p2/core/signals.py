"""p2 signals"""
import hashlib
from logging import getLogger

from django.core.signals import Signal
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from p2.core import constants
from p2.core.models import Blob

LOGGER = getLogger(__name__)

BLOB_PAYLOAD_UPDATED = Signal(providing_args=['blob'])
BLOB_ACCESS = Signal(providing_args=['status_code', ''])
BLOB_PRE_SAVE = Signal(providing_args=['blob'])
BLOB_POST_SAVE = Signal(providing_args=['blob'])

BUF_SIZE = 65536


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
    instance.volume.storage.controller.delete(instance)

@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def blob_payload_hash(sender, blob, **kwargs):
    """Add common hashes as attributes"""
    hashes = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha256': hashlib.sha256(),
        'sha384': hashlib.sha384(),
        'sha512': hashlib.sha512(),
    }
    # Check if any values were updated to prevent recursive saving
    while True:
        data = blob.read(BUF_SIZE)
        if not data:
            break
        for hash_name in hashes:
            hashes[hash_name].update(data)
    for hash_name in hashes:
        _hash = hashes[hash_name].hexdigest()
        attr_name = getattr(constants, 'ATTR_BLOB_HASH_%s' % hash_name.upper())
        if attr_name not in blob.attributes or blob.attributes[attr_name] != _hash:
            blob.attributes[attr_name] = _hash
            LOGGER.debug('Updated %s for %s to %s',
                         hash_name, blob.uuid.hex, _hash)
    blob.save()
