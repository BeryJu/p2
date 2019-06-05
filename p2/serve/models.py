"""p2 Serve Models"""
import re
from logging import getLogger

from django.db import models

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

    _compiled_regex = {}

    def _regex(self, key):
        """Compiled regex and cache instance"""
        if key not in self._compiled_regex:
            self._compiled_regex[key] = re.compile(self.tags.get(key, ""))
        return self._compiled_regex[key]

    def matches(self, request):
        """Return true if request matches our tags, false if not"""
        for tag_key, tag_value in self.tags.items():
            request_value = None
            if tag_key == TAG_SERVE_MATCH_PATH:
                request_value = request.path
            elif tag_key == TAG_SERVE_MATCH_PATH_RELATIVE:
                request_value = request.path[1:]
            elif tag_key == TAG_SERVE_MATCH_HOST:
                request_value = request.META.get('HTTP_HOST')
            elif tag_key.startswith(TAG_SERVE_MATCH_META):
                meta_key = tag_key.replace(TAG_SERVE_MATCH_META, '')
                request_value = request.META.get(meta_key, '')
            LOGGER.debug("Checking %s against %s", request_value, tag_value)
            if not self._regex(tag_key).match(request_value):
                LOGGER.debug("  => Not matching")
                return False
        return True

    def __str__(self):
        return "ServeRule %s" % self.name
