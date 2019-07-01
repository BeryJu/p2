"""p2 Serve Models"""
import re
from logging import getLogger

from django.db import models

from p2.grpc.protos.serve_pb2 import ServeRequest
from p2.lib.models import TagModel, UUIDModel
from p2.serve.constants import (TAG_SERVE_MATCH_HOST, TAG_SERVE_MATCH_META,
                                TAG_SERVE_MATCH_PATH,
                                TAG_SERVE_MATCH_PATH_RELATIVE)

LOGGER = getLogger(__name__)

class ServeRule(TagModel, UUIDModel):
    """ServeRule which converts a URL matching a regular expression toa database lookup"""

    PREDEFINED_TAGS = {
        TAG_SERVE_MATCH_PATH_RELATIVE: ''
    }

    name = models.TextField()
    blob_query = models.TextField()

    def matches(self, request: ServeRequest):
        """Return true if request matches our tags, false if not"""
        for tag_key, tag_value in self.tags.items():
            request_value = None
            if tag_key == TAG_SERVE_MATCH_PATH:
                request_value = request.url
            elif tag_key == TAG_SERVE_MATCH_PATH_RELATIVE:
                request_value = request.url[1:]
            elif tag_key == TAG_SERVE_MATCH_HOST:
                request_value = request.headers.get('Host', '')
            elif tag_key.startswith(TAG_SERVE_MATCH_META):
                meta_key = tag_key.replace(TAG_SERVE_MATCH_META, '')
                request_value = request.headers.get(meta_key, '')
            LOGGER.debug("Checking '%s' against '%s'", request_value, tag_value)
            regex = re.compile(tag_value)
            match = regex.match(request_value)
            if match is None:
                LOGGER.debug("  => Not matching")
                return False
            LOGGER.debug("  => Matching, checking next tag")
        return True

    def __str__(self):
        return "ServeRule %s" % self.name
