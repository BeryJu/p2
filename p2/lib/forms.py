"""p2 form helpers"""
import json

from django import forms


class TagModelForm(forms.ModelForm):
    """Base form for models that inherit p2.lib.models.TagModel"""

    def __init__(self, *args, **kwargs):
        # Check if we have an instance, load tags otherwise use an empty dict
        instance = kwargs.get('instance', None)
        tags = instance.tags if instance else {}
        # Make sure all predefined tags exist in tags, and set default if they don't
        predefined_tags = self._meta.model().get_predefined_tags()  # pylint: disable=no-member
        for key, value in predefined_tags.items():
            if key not in tags:
                tags[key] = value
        # Format JSON
        kwargs['initial']['tags'] = json.dumps(tags, indent=4, sort_keys=True)
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        """Make sure all required tags are set"""
        if hasattr(self.instance, 'get_required_keys') and hasattr(self.instance, 'tags'):
            for key in self.instance.get_required_keys():
                if key not in self.cleaned_data.get('tags'):
                    raise forms.ValidationError("Tag %s missing." % key)
        return self.cleaned_data.get('tags')
