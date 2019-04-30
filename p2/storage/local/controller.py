"""p2 local store controller"""
import os
from logging import getLogger
from typing import Union

from p2.core.models import Blob
from p2.core.storages.base import StorageController
from p2.storage.local.constants import TAG_ROOT_PATH

LOGGER = getLogger(__name__)

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

    def retrieve_payload(self, blob: Blob) -> Union[None, bytes]:
        root = self.tags.get(TAG_ROOT_PATH)
        fs_path = os.path.join(root, self._build_subdir(blob), blob.uuid.hex)
        LOGGER.debug('RETR "%s"', blob.uuid)
        if os.path.exists(fs_path) and os.path.isfile(fs_path):
            LOGGER.debug("  -> Opening '%s' for retrival.", fs_path)
            with open(fs_path, 'rb') as _file:
                return _file.read()
        else:
            LOGGER.warning(
                "File '%s' does not exist or is not a file.", fs_path)
        return None

    def update_payload(self, blob: Blob, payload: Union[None, bytes]):
        root = self.tags.get(TAG_ROOT_PATH)
        fs_path = os.path.join(root, self._build_subdir(blob), blob.uuid.hex)
        os.makedirs(os.path.dirname(fs_path), exist_ok=True)
        LOGGER.debug('UPDT "%s" "%.5s"', blob.uuid, payload)
        if not payload:
            # Not payload, delete file if it exists
            if os.path.exists(fs_path) and os.path.isfile(fs_path):
                os.unlink(fs_path)
                LOGGER.debug("  -> Deleted '%s'.", fs_path)
            else:
                LOGGER.warning(
                    "File '%s' does not exist during deletion attempt.", fs_path)
        else:
            LOGGER.debug("  -> Opening '%s' for updating.", fs_path)
            with open(fs_path, 'wb') as _file:
                _file.write(payload)
