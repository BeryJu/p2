"""p2 S3 HTTP Wrappers"""
from xml.etree import ElementTree

from django.http import HttpResponse

from p2.s3.errors import AWSError


class XMLResponse(HttpResponse):
    """Equivalent to JsonResponse for XML Objects"""

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'text/xml')
        data = ElementTree.tostring(data, encoding='utf-8', method='xml')
        super().__init__(content=data, **kwargs)

class AWSErrorView(XMLResponse):
    """AWS Error Response"""

    def __init__(self, error: AWSError):
        root = ElementTree.Element("Error")
        ElementTree.SubElement(root, "Code").text = error.code
        super().__init__(root, status=error.status)
