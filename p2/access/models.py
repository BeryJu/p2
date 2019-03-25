from django.db import models


class AccessRule(models.Model):

    match = models.TextField()
    blob_query = models.TextField()

    _compiled_regex = None

    def __str__(self):
        return "AccessRule %s" % self.match

# tags__sha512__startswith=%(path)
