"""s3 forms"""
from django import forms

from p2.s3.models import S3AccessKey


class S3AccessKeyForm(forms.ModelForm):
    """S3 Access Key form"""

    # TODO: Automatically pre-fill access_key and secret_key

    class Meta:

        model = S3AccessKey
        fields = ['name', 'user', 'access_key', 'secret_key']
        widgets = {
            'name': forms.TextInput
        }
