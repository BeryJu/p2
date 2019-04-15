"""p2 core forms"""
from django import forms

from p2.core.models import BaseStorage, Blob, Volume


class BlobForm(forms.ModelForm):
    """blob form"""

    payload = forms.FileField()

    class Meta:

        model = Blob
        fields = ['path', 'payload', 'volume', 'tags']
        widgets = {
            'path': forms.TextInput
        }


class BaseStorageForm(forms.ModelForm):
    """storage form"""

    class Meta:

        model = BaseStorage
        fields = '__all__'


class VolumeForm(forms.ModelForm):
    """volume form"""

    class Meta:

        model = Volume
        fields = ['name', 'storage', 'tags']
        widgets = {
            'name': forms.TextInput
        }
