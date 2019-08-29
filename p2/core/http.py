"""p2 core http responses"""
from wsgiref.util import FileWrapper

from django.http import StreamingHttpResponse

from p2.core.constants import ATTR_BLOB_MIME, ATTR_BLOB_SIZE_BYTES
from p2.core.models import Blob


class BlobResponse(StreamingHttpResponse):
    """Directly return blob's content. Optionally return as attachment if as_download is True"""

    def __init__(self, blob: Blob, chunk_size=8192):
        super().__init__(FileWrapper(blob, chunk_size))
        self['Content-Length'] = blob.attributes.get(ATTR_BLOB_SIZE_BYTES, 0)
        self['Content-Type'] = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
