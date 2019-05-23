"""p2 core component forms"""
from django import forms

from p2.core.models import Component
from p2.lib.models import UUIDModel


# pylint: disable=too-few-public-methods
class ComponentFormMeta:
    """Base meta class, set common fields"""

    model = Component
    fields = ['enabled']
    field_map = {
        # Map of field_name: tag_name of instance to load/save
    }
    defaults = {
        # (optional) Map of field_name: default value if tag is not set
    }


class ComponentForm(forms.ModelForm):
    """Base form for all Component forms, adds a load(self, instance) method to fill fields"""

    def load(self, instance):
        """Load self.fields[x] from instance.tags"""
        for field_name, tag in self.Meta.field_map.items():
            default_value = self.Meta.defaults.get(field_name, '')
            self.fields[field_name].initial = instance.tags.get(tag, default_value)

    def save(self):
        for field_name, tag in self.Meta.field_map.items():
            value = self.cleaned_data.get(field_name)
            if isinstance(value, UUIDModel):
                self.instance.tags[tag] = value.uuid.hex
            else:
                self.instance.tags[tag] = value
        return super().save()

    class Meta(ComponentFormMeta):
        pass
