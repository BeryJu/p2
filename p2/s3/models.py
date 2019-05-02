"""p2 S3 models"""
import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


def get_access_key():
    """Generate random string to use as access key"""
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(letters) for i in range(20))

def get_secret_key():
    """Generate random string to use as secret key"""
    letters = string.ascii_lowercase + string.ascii_uppercase + \
        string.digits + string.punctuation
    return ''.join(random.SystemRandom().choice(letters) for i in range(40))

class S3AccessKey(models.Model):
    """S3 Access Key"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    access_key = models.CharField(max_length=20, default=get_access_key)
    secret_key = models.CharField(max_length=40, default=get_secret_key)

    def __str__(self):
        return "Access Key %s for user %s" % (self.name, self.user.username)

    class Meta:
        verbose_name = _('S3 Access Key')
        verbose_name_plural = _('S3 Access Keys')
        unique_together = (('access_key', 'secret_key'),)
