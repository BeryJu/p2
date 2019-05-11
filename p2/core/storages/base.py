"""p2 storage base controller"""
from io import RawIOBase

from p2.core.controllers import Controller
from p2.core.models import Blob


class StorageController(Controller):
    """Base Storage Controller Class"""

    form_class = 'p2.core.forms.StorageForm'

    def collect_attributes(self, blob: Blob):
        """Collect stats like size and mime type. This is being called during Blob's save"""

    def retrieve_payload(self, blob: Blob) -> RawIOBase:
        """Return file-like object which can be used to manipulate payload."""
        raise NotImplementedError

    def update_payload(self, blob: Blob, file_like: RawIOBase):
        """Write data from file-like object."""
        raise NotImplementedError
