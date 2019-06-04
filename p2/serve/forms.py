"""serve forms"""
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from p2.lib.forms import TagModelForm, TagModelFormMeta
from p2.serve.models import ServeRule


class ServeRuleForm(TagModelForm):
    """Serve Rule Form"""

    class Meta(TagModelFormMeta):

        model = ServeRule
        fields = ['name', 'tags', 'blob_query']
        widgets = {
            'name': forms.TextInput,
            'blob_query': forms.TextInput,
        }
        help_texts = {
            'blob_query': mark_safe(_("""
            The placeholder '{path}' will be replaced with the request path.
            '{host} will be replaced by the used hostname.
            You can also use {meta[X]} where X is any of the fields
            described <a href="https://docs.djangoproject.com/en/2.2/ref/request-response
            /#django.http.HttpRequest.META">here</a>"""))
        }


class ServeRuleDebugForm(forms.Form):
    """Debug ServeRule's blob_query"""

    path = forms.CharField()
    result = forms.CharField(widget=forms.Textarea(attrs={'readonly':True}), required=False)
