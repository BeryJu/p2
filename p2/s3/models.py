"""p2 s3 models"""
from logging import getLogger
from os import unlink
from tempfile import mkstemp
from uuid import uuid4

from django.db import models

from p2.core.models import Volume
from p2.lib.models import UUIDModel

LOGGER = getLogger(__name__)

def make_temp_path():
    """Get temporary file"""
    _handle, path = mkstemp(suffix='_p2_s3_multipart')
    LOGGER.debug("Temporary Multipart File: '%s'", path)
    return path

class MultipartUpload(models.Model):
    """Initiated multipart upload, holding multiple parts"""

    upload_id = models.UUIDField(primary_key=True, default=uuid4)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    blob_key = models.TextField()

    class Meta:

        unique_together = (('volume', 'blob_key'),)


class MultipartUploadPart(UUIDModel):
    """Single part of MultipartUpload"""

    upload = models.ForeignKey(MultipartUpload, on_delete=models.CASCADE)
    part = models.IntegerField()
    temporary_file_path = models.TextField(default=make_temp_path)

    _handle = None

    @property
    def temporary_file(self):
        """Open binary write handle to temporary file"""
        if not self._handle:
            self._handle = open(self.temporary_file_path, 'r+b')
        return self._handle

    def cleanup(self):
        """Delete temporary file"""
        # FIXME: Convert this to a pre_delete signal
        unlink(self.temporary_file_path)

    class Meta:

        unique_together = (('upload', 'part'),)
