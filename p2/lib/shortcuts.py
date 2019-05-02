"""p2 lib shortcuts"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user


def get_object_for_user_or_404(user, permission, **filters):
    """Wrapper around get_object_or_404 that checks permissions"""
    return get_object_or_404(get_objects_for_user(user, permission), **filters)


def get_list_for_user_or_404(user, permission, **filters):
    """Wrapper around get_list_or_404 that checks permissions"""
    # We're not using the native get_list_or_404 since we want to return a queryset
    objects = get_objects_for_user(user, permission).filter(**filters)
    if not objects.exists():
        raise Http404
    return objects
