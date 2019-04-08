"""p2 log tasks"""
from p2.core.celery import CELERY_APP
from p2.log.models import LogAdaptor


@CELERY_APP.task()
def write_log_record(record):
    """Write log record to database/syslog/whatever"""
    for adaptor in LogAdaptor.objects.all().select_subclasses():
        adaptor.log(record)
