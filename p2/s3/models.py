from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class S3AccessKey(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    access_key = models.CharField(max_length=253, unique=True)
    secret_key = models.UUIDField(default=uuid4)

    def __str__(self):
        return "Access Key %s for user %r" % (self.name, self.user)

    class Meta:
        verbose_name = _('S3 Access Key')
        verbose_name_plural = _('S3 Access Keys')
