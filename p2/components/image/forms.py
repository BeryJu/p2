"""p2 image forms"""
from django import forms

from p2.components.image.constants import (DEFAULT_EXIF_TAGS,
                                           TAG_IMAGE_EXIF_TAGS)
from p2.core.components.forms import ComponentForm, ComponentFormMeta


class ImageForm(ComponentForm):
    """Image form"""

    exif_tags = forms.MultipleChoiceField(choices=[(x, x) for x in DEFAULT_EXIF_TAGS])

    class Meta(ComponentFormMeta):

        fields = ['enabled', 'exif_tags']
        field_map = {
            'exif_tags': TAG_IMAGE_EXIF_TAGS
        }
        defaults = {
            'exif_tags': DEFAULT_EXIF_TAGS
        }
