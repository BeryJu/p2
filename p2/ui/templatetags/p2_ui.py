"""p2 ui templatetags"""
import json

from django import template
from django.db.models import Model
from django.shortcuts import reverse

from p2.lib.reflection import path_to_class

register = template.Library()


@register.simple_tag(takes_context=True)
def model_app(context, expected=None):
    """Check if current view's model is the same as expected. Return "active" if both match"""
    view = context.get('view', None)
    app = None
    if hasattr(view, 'model'):
        app = view.model._meta.app_label
    return "active" if app == expected else ""

@register.filter
def model_verbose_name(model):
    """Return model's verbose_name"""
    if isinstance(model, Model):
        model = model.__class__
    return model._meta.verbose_name

@register.filter
def get_attribute(blob, path):
    """Access blob.attributes but allow keys like 'site:bytes"""
    return blob.attributes.get(path_to_class(path))


@register.filter('startswith')
def startswith(text, starts):
    """Simple wrapper for str.startswith"""
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter('json')
def json_pretty(obj):
    """Convert obj into pretty-printed JSON"""
    return json.dumps(obj, indent=4, sort_keys=True)


@register.filter('blob_url')
def blob_url(blob):
    """Return URL to blob"""
    return reverse('p2_s3:bucket-object', kwargs={
        'bucket': blob.volume.name,
        'path': blob.path[1:]
    })


@register.filter('blob_string')
def blob_string(blob):
    """Read blob's content and return as string"""
    return blob.read().decode('utf-8')
