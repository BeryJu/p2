"""p2 lib models"""
from logging import getLogger
from uuid import uuid4

from django.contrib.postgres.fields import HStoreField
from django.db import models
from p2.lib.reflection import path_to_class

LOGGER = getLogger(__name__)


class UUIDModel(models.Model):
    """Generic Model with a UUID as Primary key"""

    uuid = models.UUIDField(default=uuid4, primary_key=True)

    class Meta:

        abstract = True

class TagModel(models.Model):
    """Model which can be tagged and have pre-defined tag keys"""

    tags = HStoreField(default=dict, blank=True)

    PREDEFINED_TAGS = {}
    REQUIRED_KEYS = []

    def get_predefined_tags(self):
        """Get list of pre-defined keys, which should be set as default"""
        return self.PREDEFINED_TAGS

    def get_required_keys(self):
        """Get list of required keys. Will be checked in form"""
        return self.REQUIRED_KEYS

    class Meta:

        abstract = True

class ControllerModel(models.Model):
    """Model which has selectable controller"""

    controller_path = models.TextField()

    _controller_instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('controller_path')._choices = self.get_controller_choices()

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

    def get_controller_choices(self):
        """Get list of tuples for choices"""
        raise NotImplementedError

    class Meta:

        abstract = True
