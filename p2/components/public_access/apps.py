"""p2 PublicAccess AppConfig"""
from importlib import import_module

from django.apps import AppConfig


class P2PublicAccessComponentConfig(AppConfig):
    """p2 PublicAccess AppConfig"""

    name = 'p2.components.public_access'
    label = 'p2_components_public_access'

    def ready(self):
        super().ready()
        import_module('p2.components.public_access.signals')
