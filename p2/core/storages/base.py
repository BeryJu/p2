"""p2 storage base controller"""
from typing import Union

from p2.core.controllers import Controller
from p2.core.models import Blob


class StorageController(Controller):
    """Base Storage Controller Class"""

    form_class = 'p2.core.forms.StorageForm'

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        """Retrieve binary payload of blob. Return None if blob could not be found."""
        raise NotImplementedError

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        """Update payload of blob with binary data. If data is None, delete entry."""
        raise NotImplementedError
