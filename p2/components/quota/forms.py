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

    class Meta(ComponentFormMeta):

        fields = ['enabled', 'threshold', 'action']
        field_map = {
            'threshold': TAG_QUOTA_THRESHOLD,
            'action': TAG_QUOTA_ACTION
        }
        defaults = {
            'threshold': 0,
            'action': ACTION_NOTHING
        }
