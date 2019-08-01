"""p2 K8s App Config"""
from importlib import import_module

from django.apps import AppConfig


class P2K8sConfig(AppConfig):
    """p2 K8s App Config"""

    name = 'p2.k8s'
    label = 'p2_k8s'
    verbose_name = 'p2 K8s'

    def ready(self):
        super().ready()
        import_module('p2.k8s.component_controller')
        import_module('p2.k8s.ingress_controller')
