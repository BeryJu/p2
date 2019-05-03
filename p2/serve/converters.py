"""p2 serve URL converters"""
from django.urls.converters import StringConverter


class EverythingConverter(StringConverter):
    """Match everything"""

    regex = '(.+)'
