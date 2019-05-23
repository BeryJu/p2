"""p2 Replication AppConfig"""
from importlib import import_module

from django.apps import AppConfig


class P2ReplicationComponentConfig(AppConfig):
    """p2 Replication AppConfig"""

    name = 'p2.components.replication'
    label = 'p2_components_replication'

    def ready(self):
        super().ready()
        import_module('p2.components.replication.signals')
