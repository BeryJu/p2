"""p2 lib models"""
from uuid import uuid4

from django.db import models


class UUIDModel(models.Model):
    """Generic Model with a UUID as Primary key"""

    uuid = models.UUIDField(default=uuid4, primary_key=True)

    class Meta:

        abstract = True
