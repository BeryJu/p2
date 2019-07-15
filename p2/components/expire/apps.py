"""p2 Expire AppConfig"""
from importlib import import_module

from django.apps import AppConfig


class P2ExpireComponentConfig(AppConfig):
    """p2 Expire AppConfig"""

    name = 'p2.components.expire'
    label = 'p2_components_expire'

    def ready(self):
        super().ready()
        import_module('p2.components.expire.tasks')
        import_module('p2.components.expire.signals')
