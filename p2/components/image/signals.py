"""Image signals"""

from django.dispatch import receiver

from p2.components.image.controller import ImageController
from p2.core.signals import BLOB_PAYLOAD_UPDATED
from p2.lib.reflection import class_to_path


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def payload_updated_exif(sender, blob, **kwargs):
    """extract EXIF data from image and save as attributes"""
    image_component = blob.volume.component_set.filter(controller=class_to_path(ImageController))
    if image_component.exists():
        image_component.first().handle(blob)
