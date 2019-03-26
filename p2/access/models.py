from re import compile

from django.db import models


class AccessRule(models.Model):

    match = models.TextField()
    blob_query = models.TextField()

    _compiled_regex = None

    @property
    def regex(self):
        if not self._compiled_regex:
            self._compiled_regex = compile(self.match)
        return self._compiled_regex

    def __str__(self):
        return "AccessRule %s" % self.match

# tags__sha512__startswith=%(path)
