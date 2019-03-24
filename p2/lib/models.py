from uuid import uuid4

from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)

    class Meta:

        abstract = True
