"""Image signals"""
from io import BytesIO
from logging import getLogger

from django.dispatch import receiver
from PIL import ExifTags, Image

from p2.core.signals import BLOB_PAYLOAD_UPDATED

LOGGER = getLogger(__name__)


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def payload_updated_exif(sender, blob, **kwargs):
    """extract EXIF data from image and save as attributes"""
    try:
        img = Image.open(BytesIO(blob.payload))
        # Remove all keys starting with EXIF: to prevent stale keys
        for key in list(blob.attributes.keys()):
            if key.startswith('exif:'):
                del blob.attributes[key]
        # Read out EXIF attributes, lookup numerical EXIF name and save as key exif:x
        # pylint: disable=protected-access
        if hasattr(img, '_getexif'):
            # pylint: disable=protected-access
            exif_data = img._getexif()
            if exif_data:
                exif = {
                    'exif:%s' % ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS and isinstance(v, str)
                }
                blob.attributes.update(exif)
                LOGGER.debug("Updated EXIF data")
    except IOError:
        LOGGER.debug("Blob '%s' is not an image, skipping EXIF.", blob.uuid)
