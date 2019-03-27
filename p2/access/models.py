"""p2 Access Models"""
import re

from django.db import models


class AccessRule(models.Model):
    """AccessRule which converts a URL matching a regular expression toa database lookup"""

    match = models.TextField()
    blob_query = models.TextField()

    _compiled_regex = None

    @property
    def regex(self):
        """Compiled regex and cache instance"""
        if not self._compiled_regex:
            self._compiled_regex = re.compile(self.match)
        return self._compiled_regex

    def __str__(self):
        return "AccessRule %s" % self.match
