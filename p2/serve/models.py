"""p2 Serve Models"""
import re

from django.db import models


class ServeRule(models.Model):
    """ServeRule which converts a URL matching a regular expression toa database lookup"""

    name = models.TextField()
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
        return "ServeRule %s" % self.name
