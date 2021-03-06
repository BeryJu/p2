"""p2 Quota App Config"""
from importlib import import_module

from django.apps import AppConfig


class P2QuotaComponentConfig(AppConfig):
    """p2 Quota App Config"""

    name = 'p2.components.quota'
    label = 'p2_components_quota'
    verbose_name = 'p2 Quota Component'

    def ready(self):
        super().ready()
        import_module('p2.components.quota.signals')
