"""p2 import controller"""
from logging import getLogger

from PIL import ExifTags, Image

from p2.core.components.base import ComponentController

LOGGER = getLogger(__name__)

# pylint: disable=too-few-public-methods
class ImageController(ComponentController):
    """add image attributes from exif data"""

    template_name = 'components/image/card.html'
    form_class = 'p2.components.image.forms.ImageForm'

    def handle(self, blob):
        """extract EXIF data from image and save as attributes"""
        try:
            img = Image.open(blob)
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
