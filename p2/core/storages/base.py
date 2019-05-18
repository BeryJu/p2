"""p2 storage base controller"""
from io import RawIOBase
from tempfile import SpooledTemporaryFile

from p2.core.controllers import Controller
from p2.core.models import Blob


class StorageController(Controller):
    """Base Storage Controller Class"""

    form_class = 'p2.core.forms.StorageForm'

    def collect_attributes(self, blob: Blob):
        """Collect stats like size and mime type. This is being called during Blob's save"""

    def get_read_handle(self, blob: Blob) -> RawIOBase:
        """Return file-like object which can be used to manipulate payload."""
        raise NotImplementedError

    # pylint: disable=unused-argument
    def get_write_handle(self, blob: Blob) -> RawIOBase:
        """Return file-like object to write data into. Default implementation opens a temporary
        file in w+b mode."""
        return SpooledTemporaryFile(max_size=500)

    def commit(self, blob: Blob, handle: RawIOBase):
        """Called when blob is saved and data can be flushed to disk/remote"""
        raise NotImplementedError

    def delete(self, blob: Blob):
        """Delete Blob"""
        raise NotImplementedError
