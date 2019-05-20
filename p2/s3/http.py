"""p2 S3 HTTP Wrappers"""
from xml.etree import ElementTree

from django.http import HttpResponse


class XMLResponse(HttpResponse):
    """Equivalent to JsonResponse for XML Objects"""

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'text/xml')
        data = ElementTree.tostring(data, encoding='utf-8', method='xml')
        super().__init__(content=data, **kwargs)
