"""p2 form helpers"""

from django import forms


class TagModelForm(forms.ModelForm):
    """Base form for models that inherit p2.lib.models.TagModel"""

    # TODO: Implement get_predefined_tags

    def clean_tags(self):
        """Make sure all required tags are set"""
        if hasattr(self.instance, 'get_required_keys') and hasattr(self.instance, 'tags'):
            for key in self.instance.get_required_keys():
                if key not in self.cleaned_data.get('tags'):
                    raise forms.ValidationError("Tag %s missing." % key)
        return self.cleaned_data.get('tags')
