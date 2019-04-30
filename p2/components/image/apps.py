"""p2 Image AppConfig"""
from importlib import import_module

from django.apps import AppConfig


class P2ImageComponentConfig(AppConfig):
    """p2 Image AppConfig"""

    name = 'p2.components.image'
    label = 'p2_components_image'

    def ready(self):
        super().ready()
        import_module('p2.components.image.signals')
