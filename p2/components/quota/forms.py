"""p2 quota forms"""
from django import forms
from django.utils.translation import gettext_lazy as _

from p2.components.quota.constants import (ACTION_NOTHING, ACTIONS,
                                           TAG_QUOTA_ACTION,
                                           TAG_QUOTA_THRESHOLD)
from p2.core.components.forms import ComponentForm, ComponentFormMeta


class QuotaForm(ComponentForm):
    """Quota form"""

    threshold = forms.CharField(widget=forms.NumberInput, help_text=_('Capacity in bytes'))
    action = forms.ChoiceField(choices=ACTIONS, initial=ACTION_NOTHING)

    # FIXME: This could be a generic function that is controlled with a dict

    def load(self, instance):
        self.fields['threshold'].initial = instance.tags.get(TAG_QUOTA_THRESHOLD, 0)
        self.fields['action'].initial = instance.tags.get(TAG_QUOTA_ACTION, ACTION_NOTHING)

    def save(self):
        self.instance.tags[TAG_QUOTA_ACTION] = self.cleaned_data.get('action')
        self.instance.tags[TAG_QUOTA_THRESHOLD] = self.cleaned_data.get('threshold')
        return super().save()

    class Meta(ComponentFormMeta):

        fields = ['enabled', 'threshold', 'action']
