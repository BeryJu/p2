"""serve forms"""
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from p2 import __version__
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
            'tags': mark_safe(_("""
            All of the used keys have to match the requests value for this Rule to trigger.
            You can use Regular Expressions as values. See <a target="_blank" href=
            "https://git.beryju.org/BeryJu.org/p2/blob/version/%(version)s/p2/serve/constants.py">
            here</a> for a list of all possible tags.""" % {'version':__version__})),
            'blob_query': mark_safe(_("""
            The following placeholders can be used:
            <ul>
                <li>{path} will be replaced by the full Request Path.
                This path starts with a slash.</li>
                <li>{path_relative} will be replaced by the relative Request Path.</li>
                <li>{host} will be replaced by the requested Hostname.</li>
                <li>{meta[X]} where X is any of the fields
            described <a target="_blank" href=
            "https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.META">
            here</a></li></ul>"""))
        }


class ServeRuleDebugForm(forms.Form):
    """Debug ServeRule's blob_query"""

    path = forms.CharField()
    result = forms.CharField(widget=forms.Textarea(attrs={'readonly':True}), required=False)
