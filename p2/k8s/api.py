"""p2 k8s api"""
from kubernetes.client import ApiClient
from kubernetes.config import load_incluster_config, load_kube_config
from kubernetes.config.config_exception import ConfigException
from structlog import get_logger

from p2.lib.config import CONFIG

LOGGER = get_logger()
MANAGED_BY = {
    "app.kubernetes.io/managed-by": "k8s.p2.io"
}
FIELD_MANAGER = 'k8s.p2.io'

# pylint: disable=too-few-public-methods
class APIHelper:
    """Base class with helper methods. Automatically creates client
    and provides current namespace."""

    _namespace = ""
    _client: ApiClient = None

    def __init__(self):
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
