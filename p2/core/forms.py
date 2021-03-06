"""p2 core forms"""
from django import forms
from django.core.validators import RegexValidator

from p2.core.constants import ATTR_BLOB_SIZE_BYTES
from p2.core.models import Blob, Storage, Volume
from p2.lib.forms import TagModelForm, TagModelFormMeta
from p2.lib.reflection import path_to_class


# pylint: disable=too-few-public-methods
class VolumeValidator(RegexValidator):
    """Validate volume name (s3-compatible)"""

    regex = (r'(?=^.{3,63}$)(?!^(\d+\.)+\d+$)(^(([a-z0-9]|[a-z0-9][a-z0-9\-]'
             r'*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$)')
    message = """Volume names must be at least 3 and no more than 63 characters long.
        Volume names must be a series of one or more labels.
        Volume names can contain lowercase letters, numbers, and hyphens.
        Each label must start and end with a lowercase letter or a number.
        Adjacent labels are separated by a single period (.)
        Volume names must not be formatted as an IP address (for example, 192.168.5.4)
        """

class BlobForm(TagModelForm):
    """blob form"""

    payload = forms.FileField(required=False)

    def save(self, **kwargs):
        # If payload field is empty, remove key for cleaned_data
        # so payload doesn't get overwritten
        if not self.cleaned_data.get('payload'):
            del self.cleaned_data['payload']
        instance = super().save(**kwargs)
        # If payload key still exists, a file has been selected
        # Hence we read the file and update the payload
        if 'payload' in self.cleaned_data:
            for chunk in self.cleaned_data.get('payload').chunks():
                instance.write(chunk)
            instance.attributes[ATTR_BLOB_SIZE_BYTES] = str(self.cleaned_data.get('payload').size)
        return instance

    class Meta(TagModelFormMeta):

        model = Blob
        fields = ['path', 'payload', 'tags']
        widgets = {
            'path': forms.TextInput
        }


class StorageForm(TagModelForm):
    """storage form"""

    def clean_tags(self):
        controller_class = path_to_class(self.cleaned_data.get('controller_path'))
        controller = controller_class(self.instance)
        for key in controller.get_required_tags():
            if key not in self.cleaned_data.get('tags'):
                raise forms.ValidationError("Tag '%s' missing." % key)
        return self.cleaned_data.get('tags')

    class Meta(TagModelFormMeta):

        model = Storage
        fields = ['name', 'controller_path', 'tags']
        widgets = {
            'name': forms.TextInput
        }


class VolumeForm(TagModelForm):
    """volume form"""

    name = forms.CharField(validators=[VolumeValidator()])

    class Meta(TagModelFormMeta):

        model = Volume
        fields = ['name', 'storage', 'tags']
