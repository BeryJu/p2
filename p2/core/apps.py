"""p2 app config"""
from importlib import import_module

from django.apps import AppConfig


class P2CoreConfig(AppConfig):
    """p2 main app config"""

    name = 'p2.core'
    label = 'p2_core'
    verbose_name = 'p2 Core'

    def ready(self):
        super().ready()
        import_module('p2.core.signals')
