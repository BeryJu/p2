"""p2 Core models"""
from copy import deepcopy
from logging import getLogger

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.core.serializers.json import DjangoJSONEncoder
from django.db import DatabaseError, models, transaction
from django.db.models import BigIntegerField, Sum
from django.db.models.functions import Cast
from django.utils.timezone import now
from django.utils.translation import gettext as _

from p2.core.constants import (ATTR_BLOB_SIZE_BYTES, ATTR_BLOB_STAT_CTIME,
                               ATTR_BLOB_STAT_MTIME, TAG_VOLUME_LEGACY_DEFAULT)
from p2.core.tasks import signal_marshall
from p2.lib.models import TagModel, UUIDModel
from p2.lib.reflection import class_to_path, path_to_class
from p2.lib.reflection.manager import ControllerManager

LOGGER = getLogger(__name__)
STORAGE_MANAGER = ControllerManager('storage.controllers', lazy=True)
COMPONENT_MANAGER = ControllerManager('component.controllers', lazy=True)

class Volume(UUIDModel, TagModel):
    """Folder-like object, holding a collection of blobs"""

    name = models.SlugField(unique=True)
    storage = models.ForeignKey('Storage', on_delete=models.CASCADE)

    @property
    def space_used(self):
        """Return summed up size of all blobs in this volume."""
        used = self.blob_set.all().annotate(
            size_value=Cast(KeyTextTransform(
                ATTR_BLOB_SIZE_BYTES, 'attributes'), BigIntegerField())
        ).aggregate(sum=Sum('size_value')).get('sum', 0)
        return used if used else 0

    def component(self, class_or_path):
        """Get component instance for class or class path.
        Return None if component not confugued."""
        if not isinstance(class_or_path, str):
            class_or_path = class_to_path(class_or_path)
        component = self.component_set.filter(
            controller_path=class_or_path,
            enabled=True)
        if component.exists():
            return component.first()
        return None

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
            ('list_volume_contents', 'Can List contents'),
            ('use_volume', 'Can Use Volume')
        )


# pylint: disable=too-many-instance-attributes
class Blob(UUIDModel, TagModel):
    """Binary-large object, member of a Volume and store in the volume's storage"""

    path = models.TextField()
    prefix = models.TextField()

    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    attributes = JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    _writing_handle = None
    _reading_handle = None

    class Meta:

        verbose_name = _('Blob')
        verbose_name_plural = _('Blobs')
        unique_together = (('path', 'volume',),)

    @staticmethod
    def from_uploaded_file(file, volume, prefix='/'):
        """Create Blob instance from Django's UploadedFile"""
        if not prefix.endswith('/'):
            prefix += '/'
        blob = Blob(
            path=prefix + file.name,
            volume=volume)
        for chunk in file.chunks():
            blob.write(chunk)
        blob.attributes[ATTR_BLOB_SIZE_BYTES] = str(file.size)
        blob.save()
        return blob

    @property
    def filename(self):
        """Return only the filename part of self.path"""
        return self.path.split('/')[-1]

    def _open_read_handle(self):
        if not self._reading_handle:
            self._reading_handle = self.volume.storage.controller.get_read_handle(self)

    ### File-like methods

    def read(self, *args, **kwargs):
        """Retrieve file from storage controller and call read method. Accepts same
        arguments as file's read."""
        self._open_read_handle()
        return self._reading_handle.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        """Open TemporaryFile for writing, method arguments are the same as file's write.
        File is not committed until Blob.save() is called."""
        if not self._writing_handle:
            self._writing_handle = self.volume.storage.controller.get_write_handle(self)
        return self._writing_handle.write(*args, **kwargs)

    def seek(self, pos):
        """Seek open handles to position"""
        self._open_read_handle()
        self._reading_handle.seek(pos)
        if self._writing_handle:
            self._writing_handle.seek(pos)

    def tell(self):
        """Return current position of write handle if open, otherwise read handle"""
        self._open_read_handle()
        if self._writing_handle:
            return self._writing_handle.tell()
        return self._reading_handle.tell()

    def __update_prefix(self):
        path_parts = self.path.split('/')
        self.prefix = '/'.join(path_parts[:-1])
        if self.prefix == '':
            self.prefix = '/'

    def __failsafe_path(self):
        """Make sure no path collisions can happen"""
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
        try:
            # Run update code in transaction in case
            # Storage.controller.commit fails and we need to revert
            with transaction.atomic():
                # Save current time as `created` attribute. This can be changed by users,
                # but p2.log creates a log entry for new Blob being created
                if ATTR_BLOB_STAT_CTIME not in self.attributes:
                    self.attributes[ATTR_BLOB_STAT_CTIME] = now()
                # Create/update `date_updated` attribute
                self.attributes[ATTR_BLOB_STAT_MTIME] = now()
                # Only save payload if it changed
                if self._writing_handle:
                    self._writing_handle.seek(0)
                    self.volume.storage.controller.commit(self, self._writing_handle)
                # Check if path exists already
                self.__failsafe_path()
                # Update prefix
                self.__update_prefix()
                self.volume.storage.controller.collect_attributes(self)
                super().save(*args, **kwargs)
                if self._writing_handle:
                    signal_marshall.delay('p2.core.signals.BLOB_PAYLOAD_UPDATED', kwargs={
                        'blob': {
                            'class': class_to_path(self.__class__),
                            'pk': self.uuid.hex,
                        }
                    })
        except DatabaseError:
            self.tags = _old_tags
            self.attributes = _old_attributes
            raise

    def __str__(self):
        return self.filename


class Storage(UUIDModel, TagModel):
    """Storage instance which stores blob instances."""

    name = models.TextField()
    controller_path = models.TextField(choices=STORAGE_MANAGER.as_choices())

    _controller_instance = None

    @property
    def controller(self):
        """Get instantiated controller class"""
        if not self._controller_instance:
            controller_class = path_to_class(self.controller_path)
            self._controller_instance = controller_class(self)
        return self._controller_instance

    def get_required_keys(self):
        return self.controller.get_required_tags()

    class Meta:

        verbose_name = _('Storage')
        verbose_name_plural = _('Storages')
        permissions = (
            ('use_storage', 'Can use storage'),
        )

class Component(UUIDModel, TagModel):
    """Pluggable component instance connection volume to ComponentController"""

    enabled = models.BooleanField(default=True)
    configured = True
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    controller_path = models.TextField(choices=COMPONENT_MANAGER.as_choices())

    _controller_instance = None

    @property
    def controller(self):
        """Get instantiated controller class"""
        if not self._controller_instance:
            controller_class = path_to_class(self.controller_path)
            try:
                self._controller_instance = controller_class(self)
            except (TypeError, ImportError) as exc:
                LOGGER.warning(exc)
        return self._controller_instance

    def __str__(self):
        return "%s for %s" % (self.controller.__class__.__name__, self.volume.name)

    class Meta:

        verbose_name = _('Component')
        verbose_name_plural = _('Components')
        unique_together = (('volume', 'controller_path',),)
