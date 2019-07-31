"""p2 s3 store controller"""
from io import RawIOBase
from tempfile import SpooledTemporaryFile

import boto3
from botocore.exceptions import ClientError
from structlog import get_logger

from p2.core.models import Blob
from p2.core.storages.base import StorageController
from p2.storage.s3.constants import (TAG_ACCESS_KEY, TAG_ENDPOINT, TAG_REGION,
                                     TAG_SECRET_KEY)

LOGGER = get_logger()

class S3StorageController(StorageController):
    """S3 storage controller, save blobs as files"""

    def __init__(self, instance):
        super().__init__(instance)
        session = boto3.session.Session()
        self._client = session.client(
            service_name='s3',
            aws_access_key_id=self.instance.tags.get(TAG_ACCESS_KEY),
            aws_secret_access_key=self.instance.tags.get(TAG_SECRET_KEY),
            endpoint_url=self.instance.tags.get(TAG_ENDPOINT, None),
            region_name=self.instance.tags.get(TAG_REGION))

    def get_required_tags(self):
        return [
            TAG_ACCESS_KEY,
            TAG_SECRET_KEY,
            TAG_REGION,
        ]

    def collect_attributes(self, blob: Blob):
        """Collect attributes such as size and mime type"""
        pass

    def _ensure_bucket_exists(self, name):
        """Ensure bucket exists before we attempt any object operations"""
        try:
            self._client.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.instance.tags.get(TAG_REGION)
                },
            )
        except ClientError:
            pass

    def get_read_handle(self, blob: Blob) -> RawIOBase:
        _handle = SpooledTemporaryFile()
        self._ensure_bucket_exists(blob.volume.name)
        self._client.download_fileobj(blob.volume.name, blob.path[1:], _handle)
        return _handle

    def commit(self, blob: Blob, handle: RawIOBase):
        self._ensure_bucket_exists(blob.volume.name)
        self._client.upload_fileobj(handle, blob.volume.name, blob.path[1:])

    def delete(self, blob: Blob):
        self._ensure_bucket_exists(blob.volume.name)
        self._client.delete_object(
            Bucket=blob.volume.name,
            Key=blob.path[1:])
