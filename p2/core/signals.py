"""p2 signals"""
import hashlib
from logging import getLogger

import magic
from django.core.signals import Signal
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from p2.core import constants
from p2.core.constants import ATTR_BLOB_MINE, ATTR_BLOB_SIZE_BYTES
from p2.core.models import Blob

LOGGER = getLogger(__name__)

BLOB_PAYLOAD_UPDATED = Signal(providing_args=['blob'])
BLOB_ACCESS = Signal(providing_args=['status_code', ''])


@receiver(pre_delete, sender=Blob)
# pylint: disable=unused-argument
def blob_pre_delete(sender, instance, **kwargs):
    """Tell storage to delete blob"""
    instance.volume.storage.controller.update_payload(instance, None)

@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def blob_payload_hash(sender, blob, **kwargs):
    """Add common hashes as attributes"""
    hashes = [
        'md5',
        'sha1',
        'sha256',
        'sha384',
        'sha512',
    ]
    # Check if any values were updated to prevent recursive saving
    _payload = blob.payload
    for hash_name in hashes:
        hasher = getattr(hashlib, hash_name)()
        hasher.update(_payload)
        _hash = hasher.hexdigest()
        if hash_name not in blob.attributes or blob.attributes[hash_name] != _hash:
            attr_name = getattr(constants, 'ATTR_BLOB_HASH_%s' % hash_name.upper())
            blob.attributes[attr_name] = _hash
            LOGGER.debug('Updated %s for %s to %s',
                         hash_name, blob.uuid.hex, _hash)
    blob.save()


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def blob_payload_size(sender, blob, **kwargs):
    """Add size in bytes as attribute"""
    size = len(blob.payload)
    blob.attributes[ATTR_BLOB_SIZE_BYTES] = str(size)
    LOGGER.debug('Updated size to %d for %s', size, blob.uuid.hex)
    blob.save()


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def blob_payload_mime(sender, blob, **kwargs):
    """Add mime type as attribute"""
    mime_type = magic.from_buffer(blob.payload, mime=True)
    blob.attributes[ATTR_BLOB_MINE] = mime_type
    LOGGER.debug('Updated MIME to %s for %s', mime_type, blob.uuid.hex)
    blob.save()
