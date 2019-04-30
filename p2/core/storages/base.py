"""p2 storage base controller"""
from typing import Union

from p2.core.models import Blob


class StorageController:
    """Base Storage Controller Class"""

    tags = {}

    def __init__(self, storage_instance):
        super().__init__()
        self.tags = storage_instance.tags

    def get_required_tags(self):
        """Get a list of required tags, these tags can be used to set a
        path or to save credentials or other"""
        return []

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        """Retrieve binary payload of blob. Return None if blob could not be found."""
        raise NotImplementedError

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        """Update payload of blob with binary data. If data is None, delete entry."""
        raise NotImplementedError
