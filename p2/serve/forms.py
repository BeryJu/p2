"""serve forms"""
from django import forms
from django.utils.translation import gettext_lazy as _

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
        help_texts = {
            'blob_query': _("The placeholder '%(path)s' will be replaced with the request path.")
        }
