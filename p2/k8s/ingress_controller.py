"""p2 k8s ingress Controller"""

from kubernetes.client import ExtensionsV1beta1Api
from kubernetes.client.models import (ExtensionsV1beta1HTTPIngressPath,
                                      ExtensionsV1beta1HTTPIngressRuleValue,
                                      ExtensionsV1beta1IngressBackend,
                                      ExtensionsV1beta1IngressRule,
                                      ExtensionsV1beta1IngressSpec)

from p2.k8s.helper import FIELD_MANAGER, APIHelper

INGRESS_SELECTOR = "k8s.p2.io/main-ingress=true"

class IngressController(APIHelper):

    _extensions_client: ExtensionsV1beta1Api = None
    _name = ""

    def __init__(self):
        super().__init__()
        self._extensions_client = ExtensionsV1beta1Api(self._client)
        self._name = self._find_ingress()

    def _find_ingress(self):
        ingress = self._extensions_client.list_namespaced_ingress(
            self._namespace, label_selector=INGRESS_SELECTOR).items[0]
        return ingress.metadata.name

    @property
    def domains(self):
        """Get list of all domains assigned with this ingress"""
        ingress = self._extensions_client.read_namespaced_ingress(self._name, self._namespace)
        for rule in ingress.spec.rules:
            for path in rule.http.paths:
                if path.backend.service_name.endswith('tier0'):
                    print(f"Domain {rule.host} configured for tier0")
                elif path.backend.service_name.endswith('web'):
                    print(f"Domain {rule.host} configured for web/s3")

INGRESS_CONTROLLER = IngressController()
INGRESS_CONTROLLER.domains
