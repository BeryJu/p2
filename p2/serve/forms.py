"""serve forms"""
from django import forms

from p2.serve.models import ServeRule


class ServeRuleForm(forms.ModelForm):
    """Serve Rule Form"""

    class Meta:

        model = ServeRule
        fields = '__all__'
