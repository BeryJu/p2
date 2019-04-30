"""p2 Core models"""
from copy import deepcopy
from logging import getLogger
from typing import Union

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import DatabaseError, models, transaction
from django.db.models import IntegerField, Sum
from django.db.models.functions import Cast
from django.utils.timezone import now
from django.utils.translation import gettext as _
from model_utils.managers import InheritanceManager

from p2.core.constants import TAG_VOLUME_LEGACY_DEFAULT
from p2.lib.reflection.manager import ControllerManager
from p2.core.tasks import signal_marshall
from p2.lib.models import TagModel, UUIDModel, ControllerModel
from p2.lib.reflection import class_to_path

LOGGER = getLogger(__name__)
STORAGE_MANAGER = ControllerManager('storage.controllers', lazy=True)
COMPONENT_MANAGER = ControllerManager('component.controllers', lazy=True)

class Volume(UUIDModel, TagModel):
    """Folder-like object, holding a collection of blobs"""

    name = models.SlugField()
    storage = models.ForeignKey('Storage', on_delete=models.CASCADE)

    @property
    def space_used(self):
        """Return summed up size of all blobs in this volume."""
        used = self.blob_set.all().annotate(
            size_value=Cast(KeyTextTransform('size:bytes', 'attributes'), IntegerField())
        ).aggregate(sum=Sum('size_value')).get('sum', 0)
        return used if used else 0

    def get_predefined_tags(self):
        return {
            TAG_VOLUME_LEGACY_DEFAULT: False
        }

    def __str__(self):
        return "Volume %s on %s" % (self.name, self.storage)

    class Meta:

        verbose_name = _('Volume')
        verbose_name_plural = _('Volumes')
        permissions = (
            ('list_contents', 'List contents'),
            ('use_volume', 'Use Volume')
        )


# pylint: disable=too-many-instance-attributes
class Blob(UUIDModel, TagModel):
    """Binary-large object, member of a Volume and store in the volume's storage"""

    path = models.TextField()
    prefix = models.TextField()

    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    attributes = JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    _payload = None
    _payload_dirty = False

    _casted_storage = None

    class Meta:

        verbose_name = _('Blob')
        verbose_name_plural = _('Blobs')
        unique_together = (('path', 'volume',),)

    @property
    def storage_instance(self):
        """Return casted instance of storage"""
        if not self._casted_storage:
            self._casted_storage = Storage.objects.get_subclass(pk=self.volume.storage.pk)
        return self._casted_storage

    @property
    def filename(self):
        """Return only the filename part of self.path"""
        return self.path.split('/')[-1]

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

    def __update_prefix(self):
        path_parts = self.path.split('/')
        self.prefix = '/'.join(path_parts[:-1])
        if self.prefix == '':
            self.prefix = '/'

    def __failsafe_path(self):
        same_path = Blob.objects.filter(path=self.path, volume=self.volume)
        if same_path.exists() and same_path.first() != self:
            self.path = self.path + '.1'
            self.__failsafe_path()

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
                if 'stat:ctime' not in self.attributes:
                    self.attributes['stat:ctime'] = now()
                # Create/update `date_updated` attribute
                self.attributes['stat:mtime'] = now()
                # Only save payload if it changed
                if self._payload_dirty:
                    self.storage_instance.update_payload(self, self.payload)
                # Check if path exists already
                self.__failsafe_path()
                # Update prefix
                self.__update_prefix()
                super().save(*args, **kwargs)
                if self._payload_dirty:
                    signal_marshall.delay('p2.core.signals.BLOB_PAYLOAD_UPDATED', kwargs={
                        'blob': {
                            'class': class_to_path(self.__class__),
                            'pk': self.uuid.hex,
                        }
                    })
                # Only reset _payload_dirty after save so it can still be accessed in signals
                self._payload_dirty = False
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
        return self.filename


class Storage(ControllerModel, UUIDModel, TagModel):
    """Storage instance which stores blob instances."""

    name = models.TextField()

    objects = InheritanceManager()

    def get_controller_choices(self):
        return STORAGE_MANAGER.as_choices()

    def get_required_keys(self):
        return self.controller.get_required_tags()

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        """Fetch binary payload for <blob>, return None if payload doesn't exist"""
        return self.controller.retrieve_payload(blob)

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        """Update binary payload for <blob> with <payload>, if <payload> is None, delete it."""
        return self.controller.update_payload(blob, payload)

    class Meta:

        verbose_name = _('Storage')
        verbose_name_plural = _('Storages')
        permissions = (
            ('use_storage', 'Can use storage'),
        )

class Component(ControllerModel, UUIDModel, TagModel):
    """Pluggable component instance connection volume to ComponentController"""

    enabled = models.BooleanField(default=True)
    configured = True
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)

    def get_controller_choices(self):
        return COMPONENT_MANAGER.as_choices()

    def __str__(self):
        return "%s for %s" % (self.controller.__class__.__name__, self.volume.name)

    class Meta:

        verbose_name = _('Component')
        verbose_name_plural = _('Components')
        unique_together = (('volume', 'controller_path',),)
