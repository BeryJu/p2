"""p2 Core models"""
import os
from copy import deepcopy
from logging import getLogger
from typing import Union

from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import DatabaseError, models, transaction
from django.utils.timezone import now
from model_utils.managers import InheritanceManager

from p2.lib.models import TagModel, UUIDModel

LOGGER = getLogger(__name__)

class Volume(UUIDModel, TagModel):
    """Folder-like object, holding a collection of blobs"""

    PREDEFINED_KEYS = [
        'legacy-default.volume.p2.io'
    ]

    name = models.SlugField()
    storage = models.ForeignKey('BaseStorage', on_delete=models.CASCADE)

    def __str__(self):
        return "Volume %s on %s" % (self.name, self.storage)

    class Meta:
        permissions = (
            ('list_contents', 'List contents'),
            ('use_volume', 'Use Volume')
        )


class Blob(UUIDModel, TagModel):
    """Binary-large object, member of a Volume and store in the volume's storage"""

    # TODO: automatically add windows-like (1), (2), etc to paths when duplicated
    path = models.TextField()

    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    attributes = JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    _payload = None
    _payload_dirty = False

    _casted_storage = None

    class Meta:

        unique_together = (('path', 'volume',),)

    @property
    def storage_instance(self):
        """Return casted instance of storage"""
        if not self._casted_storage:
            self._casted_storage = BaseStorage.objects.get_subclass(pk=self.volume.storage.pk)
        return self._casted_storage

    @property
    def payload(self) -> bytes:
        """Retrieve binary payload from storage and cache in class instance"""
        if not self._payload:
            # Check if UUID payload is in cache
            cached_payload = cache.get(self.uuid)
            if cached_payload:
                self._payload = cached_payload
            self._payload = self.storage_instance.retrieve_payload(self)
            # Initialize a new Payload if backend has nothing saved
            if not self._payload:
                self._payload = b''
            cache.set(self.uuid, self._payload)
        return self._payload

    @payload.setter
    def payload(self, new_payload: bytes):
        self._payload_dirty = True
        self._payload = new_payload

    def save(self, *args, **kwargs):
        """Name file on storage after generated UUID and populate initial attributes"""
        # Create a copy of the current tags and payload since
        # a failed transaction.atomic() doesn't revert object values
        _old_tags = deepcopy(self.tags)
        _old_attributes = deepcopy(self.attributes)
        _old_payload = deepcopy(self._payload)
        try:
            # Run update code in transaction in case
            # Storage.update_payload fails and we need to revert
            with transaction.atomic():
                # Save current time as `created` attribute. This can be changed by users,
                # but p2.log creates a log entry for new Blob being created
                if not self.pk:
                    self.attributes['date_created'] = now()
                # Create/update `date_updated` attribute
                self.attributes['date_updated'] = now()
                # Only save payload if it changed
                if self._payload_dirty:
                    self.storage_instance.update_payload(self, self.payload)
                super().save(*args, **kwargs)
                # Only reset _payload_dirty after save so it can still be accessed in signals
                self._payload_dirty = False
                # TODO: Dynamically assign attributes, send signal?
                # - Image attributes like resolution, DPI, color, etc
                # TODO: Use p2.lib.tasks.marshall_task instead of synchronous sending
                # blob_payload_updated.send(self, named={'blob_uuid': self.uuid.hex})
        except DatabaseError:
            self._payload = _old_payload
            self.tags = _old_tags
            self.attributes = _old_attributes
            # Roll-back saved payload
            if self._payload_dirty:
                # self._payload_dirty hasn't been reset yet, so exception was thrown
                # in super().save() -> call update with old storage
                self.storage_instance.update_payload(self, self.payload)
            raise

    def __str__(self):
        return 'Blob uuid=%s %s:/%s' % (self.uuid, self.volume.name, self.path)


class BaseStorage(UUIDModel, TagModel):
    """Storage instance which stores blob instances."""

    name = models.TextField()

    objects = InheritanceManager()

    @property
    def provider(self):
        """Provider Name for UI"""
        return None

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        """Fetch binary payload for <blob>, return None if payload doesn't exist"""
        raise NotImplementedError

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        """Update binary payload for <blob> with <payload>, if <payload> is None, delete it."""
        raise NotImplementedError

    class Meta:
        permissions = (
            ('use_storage', 'Can use storage'),
        )

class LocalFileStorage(BaseStorage):
    """Storage which stores files on local storage"""

    PREDEFINED_KEYS = ['root.fs.p2.io']

    @property
    def provider(self):
        return 'Local Filestorage'

    def _build_subdir(self, blob: Blob) -> str:
        """get 1e/2f/ from blob where UUID starts with 1e2f"""
        return os.path.sep.join([
            blob.uuid.hex[0:2],
            blob.uuid.hex[2:4]
        ])

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        root = self.tags.get('root.fs.p2.io')
        fs_path = os.path.join(root, self._build_subdir(blob), blob.uuid.hex)
        LOGGER.debug('RETR "%s"', blob.uuid)
        if os.path.exists(fs_path) and os.path.isfile(fs_path):
            LOGGER.debug("  -> Opening '%s' for retrival.", fs_path)
            with open(fs_path, 'rb') as _file:
                return _file.read()
        else:
            LOGGER.warning("File '%s' does not exist or is not a file.", fs_path)
        return None

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        root = self.tags.get('root.fs.p2.io')
        fs_path = os.path.join(root, self._build_subdir(blob), blob.uuid.hex)
        os.makedirs(os.path.dirname(fs_path), exist_ok=True)
        LOGGER.debug('UPDT "%s" "%.5s"', blob.uuid, payload)
        if not payload:
            # Not payload, delete file if it exists
            if os.path.exists(fs_path) and os.path.isfile(fs_path):
                os.unlink(fs_path)
                LOGGER.debug("  -> Deleted '%s'.", fs_path)
            else:
                LOGGER.warning("File '%s' does not exist during deletion attempt.", fs_path)
        else:
            LOGGER.debug("  -> Opening '%s' for updating.", fs_path)
            with open(fs_path, 'wb') as _file:
                _file.write(payload)
