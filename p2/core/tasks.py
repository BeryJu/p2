"""p2 core tasks"""
from p2.core.celery import CELERY_APP
from p2.lib.reflection import path_to_class


@CELERY_APP.task(bind=True)
def signal_marshall(self, signal, args=None, kwargs=None):
    """Run signal in task worker"""
    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    # Lookup PK to model instance
    for key, value in kwargs.items():
        if 'class' in value and 'pk' in value:
            model_class = path_to_class(value.get('class'))
            model_instance = model_class.objects.get(pk=value.get('pk'))
            kwargs[key] = model_instance
    signal_cls = path_to_class(signal)
    signal_cls.send(sender=self, *args, **kwargs)
