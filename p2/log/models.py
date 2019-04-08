from django.contrib.postgres.fields import JSONField
from django.db import models

from p2.lib.models import UUIDModel


class LogAdaptor(UUIDModel):

    adaptor = models.TextField()
    options = JSONField(default=dict)

    def log(self, **kwargs):
        pass

class DatabaseLogAdaptor(LogAdaptor):
    pass

class Record(UUIDModel):

    adaptor = models.ForeignKey(LogAdaptor, on_delete=models.CASCADE)
