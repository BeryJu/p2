"""p2 k8s exceptions"""

class K8sException(Exception):
    """Base Exception for all our custom k8s exceptions"""


class InvalidDeploymentScale(K8sException):
    """Deployment cannot be scaled to the requested scale"""


class DeploymentNotFound(K8sException):
    """Deployment not found"""
