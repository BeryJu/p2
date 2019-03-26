"""p2 Image AppConfig"""
from importlib import import_module

from django.apps import AppConfig


class P2ImageConfig(AppConfig):
    """p2 Image AppConfig"""

    name = 'p2.image'
    label = 'p2_image'

    def ready(self):
        super().ready()
        import_module('p2.image.signals')
