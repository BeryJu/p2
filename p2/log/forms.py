"""p2 log forms"""
from django import forms

from p2.lib.forms import TagModelForm
from p2.lib.reflection import path_to_class
from p2.log.models import LogAdaptor


class LogAdaptorForm(TagModelForm):
    """Log Adaptor form"""

    def clean_tags(self):
        controller_class = path_to_class(self.cleaned_data.get('controller_path'))
        controller = controller_class(self.instance)
        for key in controller.get_required_tags():
            if key not in self.cleaned_data.get('tags'):
                raise forms.ValidationError("Tag '%s' missing." % key)
        return self.cleaned_data.get('tags')

    class Meta:

        model = LogAdaptor
        fields = ['name', 'controller_path', 'tags']
        widgets = {
            'name': forms.TextInput
        }
