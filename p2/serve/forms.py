"""serve forms"""
from django import forms

from p2.serve.models import ServeRule


class ServeRuleForm(forms.ModelForm):
    """Serve Rule Form"""

    class Meta:

        model = ServeRule
        fields = ['name', 'match', 'blob_query']
        widgets = {
            'name': forms.TextInput,
            'match': forms.TextInput,
            'blob_query': forms.TextInput,
        }
