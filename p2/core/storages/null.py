"""Storage Controller that does nothing"""
from io import RawIOBase

from p2.core.models import Blob
from p2.core.storages.base import StorageController


class NullStorageController(StorageController):
    """Null Storage controller, doesn't save anything, useful for debugging"""

    def get_read_handle(self, blob: Blob) -> RawIOBase:
        return None

    def get_write_handle(self, blob: Blob) -> RawIOBase:
        return None

    def commit(self, blob: Blob, handle: RawIOBase):
        return None

    def delete(self, blob: Blob):
        return None
