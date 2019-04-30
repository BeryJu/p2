"""Storage Controller that does nothing"""
from typing import Union

from p2.core.models import Blob
from p2.core.storages.base import StorageController


class NullStorageController(StorageController):
    """Null Storage controller, doesn't save anything, useful for debugging"""

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        return None

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        return None
