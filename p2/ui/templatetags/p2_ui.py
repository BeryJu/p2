"""p2 ui templatetags"""
import json

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers import registry
from django import template
from django.db.models import Model
from django.shortcuts import reverse

from p2.lib.config import CONFIG
from p2.lib.reflection import path_to_class

register = template.Library()


@register.simple_tag(takes_context=True)
def model_app(context, expected=''):
    """Check if current view's model is the same as expected. Return "active" if both match"""
    view = context.get('view', None)
    app, object_name = '', ''
    if hasattr(view, 'model'):
        app = view.model._meta.app_label
        object_name = view.model._meta.object_name
    # If expected is only a string treat it as app_label, if it contains a colon
    # treat it as app_label:model_label
    if ':' in expected:
        expected_app, expected_model = expected.split(':')
        return "active" if expected_app == app and expected_model == object_name else ""
    return "active" if app == expected else ""

@register.simple_tag
def config(key, default=None):
    """Get config value"""
    return CONFIG.y(key, default=default)

@register.simple_tag
def configured_providers():
    """Get list of providers which are actually configured"""
    providers = registry.get_list()
    configured = []
    for provider in providers:
        if SocialApp.objects.filter(provider=provider.id).exists():
            configured.append(provider)
    return configured

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
