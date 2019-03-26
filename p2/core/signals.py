"""p2 signals"""
import hashlib
from io import BytesIO
from logging import getLogger

import magic
# from p2.lib.signals import WorkerSignal
from django.core.signals import Signal
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from p2.core.models import Blob
from p2.lib.utils import url_b64encode

BUF_SIZE = 65536
LOGGER = getLogger(__name__)

blob_payload_updated = Signal(providing_args=['blob'])
blob_access = Signal(providing_args=['status_code', ''])


@receiver(pre_save, sender=Blob)
def blob_pre_save(sender, instance, **kwargs):
    if instance._payload_dirty:
        blob_payload_updated.send(sender=sender, blob=instance)

@receiver(pre_delete, sender=Blob)
def blob_pre_delete(sender, instance, **kwargs):
    instance.storage_instance.update_payload(instance, None)

@receiver(blob_payload_updated)
def blob_payload_hash(sender, blob, **kwargs):
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
            blob.attributes[hash_name] = _hash
            blob.attributes[hash_name+'_b64'] = url_b64encode(_hash)
            LOGGER.debug('Updated %s for %s to %s',
                         hash_name, blob.uuid.hex, _hash)


@receiver(blob_payload_updated)
def blob_payload_size(sender, blob, **kwargs):
    size = len(blob.payload)
    blob.attributes['size:bytes'] = str(size)
    LOGGER.debug('Updated size to %d for %s', size, blob.uuid.hex)


@receiver(blob_payload_updated)
def blob_payload_mime(sender, blob, **kwargs):
    mime_type = magic.from_buffer(blob.payload, mime=True)
    blob.attributes['mime'] = mime_type
    LOGGER.debug('Updated MIME to %s for %s', mime_type, blob.uuid.hex)
