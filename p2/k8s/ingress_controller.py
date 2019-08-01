"""p2 k8s ingress Controller"""
from typing import Optional

from kubernetes.client import CoreV1Api, ExtensionsV1beta1Api
from kubernetes.client.models import (ExtensionsV1beta1HTTPIngressPath,
                                      ExtensionsV1beta1HTTPIngressRuleValue,
                                      ExtensionsV1beta1Ingress,
                                      ExtensionsV1beta1IngressBackend,
                                      ExtensionsV1beta1IngressRule)
from structlog import get_logger

from p2.k8s.exceptions import DomainAlreadyConfigured
from p2.k8s.helper import FIELD_MANAGER, APIHelper

LOGGER = get_logger()
INGRESS_SELECTOR = "k8s.p2.io/main-ingress=true"
SERVICE_SELECTOR = "k8s.p2.io/component=%s"

class IngressController(APIHelper):
    """Add/remove domains from ingress"""

    _extensions_client: ExtensionsV1beta1Api = None
    _core_client: CoreV1Api = None
    _name = ""

    def __init__(self):
        super().__init__()
        self._extensions_client = ExtensionsV1beta1Api(self._client)
        self._core_client = CoreV1Api(self._client)
        self._name = self._find_ingress()

    def _find_ingress(self) -> str:
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

    def _get_service(self, service_label: str) -> Optional[str]:
        services = self._core_client.list_namespaced_service(
            self._namespace, label_selector=SERVICE_SELECTOR % service_label)
        if not services.items:
            return None
        return services.items[0].metadata.name

    def _check_if_domain_used(self, domain: str,
                              ingress: ExtensionsV1beta1Ingress, soft_fail=False) -> bool:
        """Check if domain is already used in this ingress.
        If Domain is used, and soft_fail is set to False (default), a
        DomainAlreadyConfigured error will be raised"""
        # Make sure domain is not configured yet
        for rule in ingress.spec.rules:
            if rule.host == domain:
                if soft_fail:
                    LOGGER.info("Domain already configured", domain=domain)
                    return False
                raise DomainAlreadyConfigured
        return True

    def add_tier0_domain(self, domain, soft_fail=False) -> bool:
        """Add domain for use with tier0"""
        ingress = self._extensions_client.read_namespaced_ingress(self._name, self._namespace)
        if not self._check_if_domain_used(domain, ingress, soft_fail=soft_fail):
            return False
        ingress.spec.rules.append(
            ExtensionsV1beta1IngressRule(
                host=domain,
                http=ExtensionsV1beta1HTTPIngressRuleValue(
                    paths=[
                        ExtensionsV1beta1HTTPIngressPath(
                            backend=ExtensionsV1beta1IngressBackend(
                                service_name=self._get_service('tier0'),
                                service_port='http'),
                            path='/'
                        )
                    ]
                )
            )
        )
        self._extensions_client.patch_namespaced_ingress(
            self._name, self._namespace, ingress, field_manager=FIELD_MANAGER)
        LOGGER.debug("Successfully configured domain for tier0", domain=domain)
        return True

    def add_default_domain(self, domain, soft_fail=False) -> bool:
        """Add domain for use with S3 or web-ui"""
        ingress = self._extensions_client.read_namespaced_ingress(self._name, self._namespace)
        if not self._check_if_domain_used(domain, ingress, soft_fail=soft_fail):
            return False
        ingress.spec.rules.append(
            ExtensionsV1beta1IngressRule(
                host=domain,
                http=ExtensionsV1beta1HTTPIngressRuleValue(
                    paths=[
                        ExtensionsV1beta1HTTPIngressPath(
                            backend=ExtensionsV1beta1IngressBackend(
                                service_name=self._get_service('web'),
                                service_port='http'),
                            path='/'
                        ),
                        ExtensionsV1beta1HTTPIngressPath(
                            backend=ExtensionsV1beta1IngressBackend(
                                service_name=self._get_service('static'),
                                service_port='http'),
                            path='/_/static/'
                        )
                    ]
                )
            )
        )
        self._extensions_client.patch_namespaced_ingress(
            self._name, self._namespace, ingress, field_manager=FIELD_MANAGER)
        LOGGER.debug("Successfully configured domain for general usage.", domain=domain)
        return True

INGRESS_CONTROLLER = IngressController()
