"""p2 core forms"""
from django import forms

from p2.core.models import Blob, Storage, Volume
from p2.lib.forms import TagModelForm
from p2.lib.reflection import path_to_class


class BlobForm(TagModelForm):
    """blob form"""

    payload = forms.FileField(required=False)

    def save(self, **kwargs):
        if not self.cleaned_data.get('payload'):
            del self.cleaned_data['payload']
        return super().save(**kwargs)

    class Meta:

        model = Blob
        fields = ['path', 'payload', 'volume', 'tags']
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

    class Meta:

        model = Storage
        fields = ['name', 'controller_path', 'tags']
        widgets = {
            'name': forms.TextInput
        }


class VolumeForm(TagModelForm):
    """volume form"""

    class Meta:

        model = Volume
        fields = ['name', 'storage', 'tags']
        widgets = {
            'name': forms.TextInput
        }
