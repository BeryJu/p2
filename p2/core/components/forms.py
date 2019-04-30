"""p2 core component forms"""
from django import forms

from p2.core.models import Component


class ComponentForm(forms.ModelForm):
    """Base form for all Component forms, adds a load(self, instance) method to fill fields"""

    def load(self, instance):
        """Load self.fields[x] from instance.tags"""
        pass

# pylint: disable=too-few-public-methods
class ComponentFormMeta:
    """Base meta class, set common fields"""

    model = Component
    fields = ['enabled']
