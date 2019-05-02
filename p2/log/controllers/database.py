"""p2 log database controller"""
from datetime import datetime

from pytz import UTC

from p2.log.controllers.base import LogController


class DatabaseLogController(LogController):
    """p2 log database controller"""

    def log(self, record_data):
        from p2.log.models import Record
        Record.objects.create(
            adaptor=self.instance,
            start_time=datetime.fromtimestamp(
                record_data.pop('start_time'), tz=UTC),
            end_time=datetime.fromtimestamp(
                record_data.pop('end_time', None), tz=UTC),
            request_uid=record_data.pop('uid', None),
            body=record_data)
