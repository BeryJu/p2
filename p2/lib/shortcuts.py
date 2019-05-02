"""p2 lib shortcuts"""

from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user

def get_object_for_user_or_404(user, permission, **filters):
    """Wrapper around get_object_or_404 that checks permissions"""
    return get_object_or_404(get_objects_for_user(user, permission), **filters)
