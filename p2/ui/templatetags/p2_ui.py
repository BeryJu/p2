"""p2 ui templatetags"""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def model_app(context, expected=None):
    """Check if current view's model is the same as expected. Return "active" if both match"""
    view = context.get('view', None)
    app = None
    if hasattr(view, 'model'):
        app = view.model._meta.app_label
    return "active" if app == expected else ""
