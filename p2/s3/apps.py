"""p2 S3 App Config"""
from xml.etree import ElementTree

from django.apps import AppConfig

from p2.s3.constants import XML_NAMESPACE


class P2S3Config(AppConfig):
    """p2 S3 App Config"""

    name = 'p2.s3'
    label = 'p2_s3'
    verbose_name = 'p2 S3'

    def ready(self):
        ElementTree.register_namespace("", XML_NAMESPACE)
