"""p2 k8s deployment controller"""
from typing import List

from django.conf import settings
from kubernetes.client import ApiClient, AppsV1Api, AutoscalingV2beta2Api
from kubernetes.client.models import (V1ObjectMeta,
                                      V2beta2CrossVersionObjectReference,
                                      V2beta2HorizontalPodAutoscaler,
                                      V2beta2HorizontalPodAutoscalerSpec,
                                      V2beta2MetricSpec, V2beta2MetricTarget,
                                      V2beta2ResourceMetricSource)
from kubernetes.config import load_incluster_config, load_kube_config
from kubernetes.config.config_exception import ConfigException
from structlog import get_logger

from p2.k8s.exceptions import DeploymentNotFound, InvalidDeploymentScale
from p2.lib.config import CONFIG

LOGGER = get_logger()
DEPLOYMENT_SELECTOR = 'k8s.p2.io/deployment'
MANAGED_BY = {
    "app.kubernetes.io/managed-by": "k8s.p2.io"
}
FIELD_MANAGER = 'k8s.p2.io'

class DeploymentController:
    """Controls whether a feature is enabled/disabled, the scale of it and
    Horizontal autoscaling."""

    _client: ApiClient = None
    _apps_client: AppsV1Api = None
    _autoscaling_client: AutoscalingV2beta2Api = None
    name = ""
    _namespace = ""
    _dependencies = []
    _is_optional = False

    def __init__(self, selector,
                 optional=False,
                 dependencies: List['DeploymentController'] = None):
        try:
            load_incluster_config()
        except ConfigException:
            try:
                load_kube_config()
                self._namespace = CONFIG.y('k8s_namespace')
            except TypeError:
                LOGGER.warning("Failed to load K8s configuration.")
                return
        self._client = ApiClient()
        self._apps_client = AppsV1Api(self._client)
        self._autoscaling_client = AutoscalingV2beta2Api(self._client)
        self.name = self._find_deployments(selector)
        self._is_optional = optional
        self._dependencies = dependencies or []

    def _find_deployments(self, selector_value):
        """Find deployment by matching selector"""
        deployment_list = self._apps_client.list_namespaced_deployment(
            self._namespace, label_selector=f"k8s.p2.io/deployment={selector_value}")
        if not deployment_list.items:
            raise DeploymentNotFound
        deployment = deployment_list.items[0]
        LOGGER.debug("Found deployment for selector",
                     selector=selector_value, deployment=deployment.metadata.name)
        return deployment.metadata.name

    @property
    def scale(self) -> int:
        """Get current scale from k8s"""
        return self._apps_client.read_namespaced_deployment_scale(
            self.name, self._namespace, pretty=settings.DEBUG).spec.replicas

    @scale.setter
    def scale(self, replicas: int):
        """Scale deployment"""
        if replicas < 1 and not self._is_optional:
            raise InvalidDeploymentScale
        current = self._apps_client.read_namespaced_deployment_scale(
            self.name, self._namespace, pretty=settings.DEBUG)
        current.spec.replicas = replicas
        # Before we scale, check dependencies and scale those
        if self._dependencies:
            for dependency in self._dependencies:
                LOGGER.debug("Scaled dependency", dependency=dependency.name)
                dependency.scale = replicas
        self._apps_client.patch_namespaced_deployment_scale(
            self.name, self._namespace, current, pretty=settings.DEBUG)
        LOGGER.info("Successfully scaled deployment",
                    deployment=self.name,
                    replicas=replicas)

    @property
    def status(self) -> int:
        """Return number of healthy pods"""
        deployment = self._apps_client.read_namespaced_deployment(self.name, self._namespace)
        return deployment.status.ready_replicas

    def enable_autoscaling(self, min_replicas, max_replicas):
        """Enable HPA"""
        name = f"{self.name}-hpa"
        hpa = V2beta2HorizontalPodAutoscaler(
            metadata=V1ObjectMeta(
                name=name,
                labels=MANAGED_BY
            ),
            spec=V2beta2HorizontalPodAutoscalerSpec(
                max_replicas=max_replicas,
                min_replicas=min_replicas,
                scale_target_ref=V2beta2CrossVersionObjectReference(
                    kind="Deployment",
                    name=self.name,
                    api_version="extensions/v1"
                ),
                metrics=[
                    V2beta2MetricSpec(
                        type="Resource",
                        resource=V2beta2ResourceMetricSource(
                            name="cpu",
                            target=V2beta2MetricTarget(
                                type="Utilization",
                                average_utilization=70
                            )
                        )
                    )
                ]
            )
        )
        response = self._autoscaling_client.create_namespaced_horizontal_pod_autoscaler(
            self._namespace, hpa, field_manager=FIELD_MANAGER, _preload_content=False)
        LOGGER.debug("Successfully enabled Autoscaling",
                     deployment=self.name,
                     min_replicas=min_replicas,
                     max_replicas=max_replicas)
        return response

    def disable_autoscaling(self):
        """Delete HorizontalPodAutoscaler"""
        response = self._autoscaling_client.delete_namespaced_horizontal_pod_autoscaler(
            f"{self.name}-hpa", self._namespace)
        LOGGER.debug("Successfully disabled Autoscaling",
                     deployment=self.name)
        return response

WEB_DEPLOYMENT = DeploymentController("web")
STATIC_DEPLOYMENT = DeploymentController("static")
GRPC_DEPLOYMENT = DeploymentController("grpc", optional=True)
TIER0_DEPLOYMENT = DeploymentController("tier0", optional=True, dependencies=[GRPC_DEPLOYMENT])
WORKER_DEPLOYMENT = DeploymentController("worker")
