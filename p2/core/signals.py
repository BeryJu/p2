"""p2 signals"""
import hashlib
from logging import getLogger

import magic
from django.core.signals import Signal
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from p2.core import constants
from p2.core.constants import (ATTR_BLOB_IS_TEXT, ATTR_BLOB_MIME,
                               ATTR_BLOB_SIZE_BYTES)
from p2.core.models import Blob

LOGGER = getLogger(__name__)

BLOB_PAYLOAD_UPDATED = Signal(providing_args=['blob'])
BLOB_ACCESS = Signal(providing_args=['status_code', ''])
BLOB_PRE_SAVE = Signal(providing_args=['blob'])
BLOB_POST_SAVE = Signal(providing_args=['blob'])

TEXT_CHARACTERS = str.encode("".join(list(map(chr, range(32, 127))) + list("\n\r\t\b")))

def is_text(payload):
    """Return True if file is text, else False"""
    _null_trans = bytes.maketrans(b"", b"")
    if not payload:
        # Empty files are considered text
        return True
    if b"\0" in payload:
        # Files with null bytes are likely binary
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    translation = payload.translate(_null_trans, TEXT_CHARACTERS)
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(translation)) / float(len(payload)) > 0.30:
        return False
    return True


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
    blob.attributes[ATTR_BLOB_MIME] = mime_type
    blob.attributes[ATTR_BLOB_IS_TEXT] = is_text(blob.payload)
    LOGGER.debug('Updated MIME to %s for %s', mime_type, blob.uuid.hex)
    blob.save()
