"""p2 replication controller"""
import copy
from logging import getLogger
from shutil import copyfileobj

from p2.components.replication.constants import (TAG_BLOB_SOURCE_UUID,
                                                 TAG_REPLICATION_TARGET)
from p2.core.components.base import ComponentController
from p2.core.models import Blob, Volume

LOGGER = getLogger(__name__)

# pylint: disable=too-few-public-methods
class ReplicationController(ComponentController):
    """Replicate Blobs 1:1 between volumes"""

    # TODO: Initial replication on config

    template_name = 'components/replication/card.html'
    form_class = 'p2.components.replication.forms.ReplicationForm'

    def _get_target_blob(self, source_blob):
        target_volume = Volume.objects.get(pk=self.instance.tags.get(TAG_REPLICATION_TARGET))
        # Check if there's a blob thats our source UUID as attribute
        possible_targets = Blob.objects.filter(**{
            'volume': target_volume,
            'attributes__%s' % TAG_BLOB_SOURCE_UUID: source_blob.uuid.hex})
        if possible_targets.exists():
            target_blob = possible_targets.first()
            LOGGER.debug("Found existing target blob: %s", target_blob.uuid.hex)
        else:
            LOGGER.debug("Creating new replicated blob for %s", source_blob.uuid.hex)
            target_blob = Blob.objects.create(
                path=source_blob.path,
                volume=target_volume,
                attributes={
                    TAG_BLOB_SOURCE_UUID: source_blob.uuid.hex
                })
        return target_blob

    def save(self, blob):
        """Replicate metadata save"""
        LOGGER.debug('Replicating::Save %s', blob.uuid.hex)
        target_blob = self._get_target_blob(blob)
        target_blob.path = blob.path
        for attr in ['path', 'prefix', 'attributes', 'tags']:
            # Copy all metadata to new blob
            setattr(target_blob, attr, copy.deepcopy(getattr(blob, attr)))
        # Make sure we don't erase the source uuid
        target_blob.attributes[TAG_BLOB_SOURCE_UUID] = blob.uuid.hex
        target_blob.save()

    def payload_updated(self, blob):
        """Replicate payload update"""
        LOGGER.debug('Replicating::UpdatePayload %s', blob.uuid.hex)
        target_blob = self._get_target_blob(blob)
        copyfileobj(blob, target_blob)
        target_blob.save()

    def delete(self, blob):
        """Delete remote blob"""
        LOGGER.debug('Replicating::Delete %s', blob.uuid.hex)
        target_blob = self._get_target_blob(blob)
        target_blob.delete()
