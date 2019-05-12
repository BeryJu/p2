"""Storage Controller that does nothing"""
from io import RawIOBase

from p2.core.models import Blob
from p2.core.storages.base import StorageController


class NullStorageController(StorageController):
    """Null Storage controller, doesn't save anything, useful for debugging"""

    def retrieve_payload(self, blob: Blob) -> RawIOBase:
        return None

    def update_payload(self, blob: Blob, file_like: RawIOBase):
        return None
