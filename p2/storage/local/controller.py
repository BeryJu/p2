"""p2 local store controller"""
import os
from io import RawIOBase
from logging import getLogger
from shutil import copyfileobj

import magic

from p2.core.constants import (ATTR_BLOB_IS_TEXT, ATTR_BLOB_MIME,
                               ATTR_BLOB_SIZE_BYTES)
from p2.core.models import Blob
from p2.core.storages.base import StorageController
from p2.storage.local.constants import TAG_ROOT_PATH

LOGGER = getLogger(__name__)
TEXT_CHARACTERS = str.encode("".join(list(map(chr, range(32, 127))) + list("\n\r\t\b")))

class LocalStorageController(StorageController):
    """Local storage controller, save blobs as files"""

    def get_required_tags(self):
        return [
            TAG_ROOT_PATH
        ]

    def _build_subdir(self, blob: Blob) -> str:
        """get 1e/2f/ from blob where UUID starts with 1e2f"""
        return os.path.sep.join([
            blob.uuid.hex[0:2],
            blob.uuid.hex[2:4]
        ])

    def _build_path(self, blob: Blob) -> str:
        root = self.tags.get(TAG_ROOT_PATH)
        return os.path.join(root, self._build_subdir(blob), blob.uuid.hex)

    def is_text(self, filename):
        """Return True if file is text, else False"""
        payload = open(filename, 'rb').read(512)
        _null_trans = bytes.maketrans(b"", b"")
        if not payload:
            # Empty files are considered text
            return True
        if b"\0" in payload:
            # Files with null bytes are likely binary
            return False
        # Get the non-text characters (maps a character to itself then
        # use the 'remove' option to get rid of the text characters.)
        translation = payload.translate(_null_trans, TEXT_CHARACTERS)
        # If more than 30% non-text characters, then
        # this is considered a binary file
        if float(len(translation)) / float(len(payload)) > 0.30:
            return False
        return True

    def collect_attributes(self, blob: Blob):
        """Collect attributes such as size and mime type"""
        if os.path.exists(self._build_path(blob)):
            mime_type = magic.from_file(self._build_path(blob), mime=True)
            size = os.stat(self._build_path(blob)).st_size
            blob.attributes[ATTR_BLOB_MIME] = mime_type
            blob.attributes[ATTR_BLOB_IS_TEXT] = self.is_text(self._build_path(blob))
            blob.attributes[ATTR_BLOB_SIZE_BYTES] = str(size)
            LOGGER.debug('Updated size to %d for %s', size, blob.uuid.hex)

    def get_read_handle(self, blob: Blob) -> RawIOBase:
        fs_path = self._build_path(blob)
        LOGGER.debug('RETR "%s"', blob.uuid)
        if os.path.exists(fs_path) and os.path.isfile(fs_path):
            LOGGER.debug("  -> Opening '%s' for retrival.", fs_path)
            return open(fs_path, 'rb')
        LOGGER.warning("File '%s' does not exist or is not a file.", fs_path)
        return None

    def commit(self, blob: Blob, handle: RawIOBase):
        fs_path = self._build_path(blob)
        os.makedirs(os.path.dirname(fs_path), exist_ok=True)
        LOGGER.debug('COMT "%s"', blob.uuid)
        LOGGER.debug("  -> Opening '%s' for updating.", fs_path)
        with open(fs_path, 'wb') as _dest:
            return copyfileobj(handle, _dest)

    def delete(self, blob: Blob):
        fs_path = self._build_path(blob)
        os.makedirs(os.path.dirname(fs_path), exist_ok=True)
        # Not file_like, delete file if it exists
        if os.path.exists(fs_path) and os.path.isfile(fs_path):
            os.unlink(fs_path)
            LOGGER.debug("  -> Deleted '%s'.", fs_path)
        else:
            LOGGER.warning(
                "File '%s' does not exist during deletion attempt.", fs_path)
