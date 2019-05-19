"""p2 test utils"""
from tempfile import mkdtemp

from p2.core.models import Storage
from p2.lib.reflection import class_to_path
from p2.storage.local.constants import TAG_ROOT_PATH
from p2.storage.local.controller import LocalStorageController


def get_test_storage():
    """Get fully instantiated storage"""
    storage_name = 'p2-unittest'
    storage, _ = Storage.objects.get_or_create(
        name=storage_name,
        controller_path=class_to_path(LocalStorageController),
        defaults={
            'tags': {
                TAG_ROOT_PATH: mkdtemp()
            }
        })
    return storage
