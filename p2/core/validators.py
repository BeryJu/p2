"""p2 core validators"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_blob_path(value):
    """Validate path starting with leading slash"""
    if not value.startswith('/'):
        raise ValidationError(
            _('%(value)s does not start with a slash'),
            params={'value': value}
        )
