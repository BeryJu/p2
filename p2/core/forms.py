"""p2 core forms"""
from django import forms

from p2.core.models import Blob, Storage, Volume
from p2.lib.forms import TagModelForm
from p2.lib.reflection import path_to_class


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
            instance.payload = self.cleaned_data.get('payload').read()
            instance.save()
        return instance

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
