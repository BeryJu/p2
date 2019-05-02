"""Image signals"""

from django.dispatch import receiver

from p2.components.image.controller import ImageController
from p2.core.signals import BLOB_PAYLOAD_UPDATED


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def payload_updated_exif(sender, blob, **kwargs):
    """extract EXIF data from image and save as attributes"""
    image_component = blob.volume.component(ImageController)
    if image_component:
        image_component.controller.handle(blob)
