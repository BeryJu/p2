"""p2 replication forms"""
from django import forms

from p2.components.replication.constants import (TAG_REPLICATION_IGNORE_IF,
                                                 TAG_REPLICATION_OFFSET,
                                                 TAG_REPLICATION_TARGET)
from p2.core.components.forms import ComponentForm, ComponentFormMeta
from p2.core.models import Volume


class ReplicationForm(ComponentForm):
    """Replication form"""

    # TODO: Filter permissions
    # TODO: Fix loading of this
    target = forms.ModelChoiceField(queryset=Volume.objects.all())
    offset = forms.IntegerField(min_value=0)
    ignore_if = forms.CharField(required=False)

    class Meta(ComponentFormMeta):

        fields = ['enabled', 'target', 'offset', 'ignore_if']
        field_map = {
            'target': TAG_REPLICATION_TARGET,
            'offset': TAG_REPLICATION_OFFSET,
            'ignore_if': TAG_REPLICATION_IGNORE_IF
        }
        defaults = {
            'offset': 0,
            'ignore_If': ''
        }
