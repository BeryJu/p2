"""iam forms"""

from django.contrib.auth.models import User
from django.forms import ModelForm


class UserForm(ModelForm):
    """Simple form to create users, without password (login-disabled)"""

    class Meta:

        model = User
        fields = ['username']
