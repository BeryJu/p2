"""p2 image forms"""
from django import forms

from p2.components.image.constants import (DEFAULT_EXIF_TAGS,
                                           TAG_IMAGE_EXIF_TAGS)
from p2.core.components.forms import ComponentForm, ComponentFormMeta


class ImageForm(ComponentForm):
    """Image form"""

    exif_tags = forms.MultipleChoiceField(choices=[(x, x) for x in DEFAULT_EXIF_TAGS])

    # FIXME: This could be a generic function that is controlled with a dict

    def load(self, instance):
        self.fields['exif_tags'].initial = instance.tags.get(
            TAG_IMAGE_EXIF_TAGS, DEFAULT_EXIF_TAGS)

    def save(self):
        self.instance.tags[TAG_IMAGE_EXIF_TAGS] = self.cleaned_data.get('exif_tags')
        return super().save()

    class Meta(ComponentFormMeta):

        fields = ['enabled', 'exif_tags']
