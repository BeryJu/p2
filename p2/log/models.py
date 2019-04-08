"""p2 log models"""
from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from model_utils.managers import InheritanceManager
from pytz import UTC

from p2.lib.models import UUIDModel


class LogAdaptor(UUIDModel):
    """Base Log Adaptor, doesn't write to anything"""

    options = JSONField(default=dict)

    objects = InheritanceManager()

    def log(self, record_data):
        """Write log record"""
        raise NotImplementedError()

class DatabaseLogAdaptor(LogAdaptor):
    """Database Log adaptor, writes log records into database"""

    def log(self, record_data):
        Record.objects.create(
            adaptor=self,
            start_time=datetime.fromtimestamp(record_data.pop('start_time'), tz=UTC),
            end_time=datetime.fromtimestamp(record_data.pop('end_time', None), tz=UTC),
            request_uid=record_data.pop('uid', None),
            body=record_data)

class Record(UUIDModel):
    """Log record from DatabaseLogAdaptor"""

    adaptor = models.ForeignKey(LogAdaptor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    request_uid = models.UUIDField(blank=True, null=True)
    body = JSONField(default=dict, encoder=DjangoJSONEncoder)

    def __str__(self):
        body_string = ' '.join(["%s=%s" % kv for kv in self.body.items()])
        return "[%s] [%s] %s" % (self.start_time, self.request_uid.hex, body_string)
