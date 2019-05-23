"""Replication signals"""

from django.db.models.signals import post_delete
from django.dispatch import receiver

from p2.components.replication.controller import ReplicationController
from p2.core.models import Blob
from p2.core.signals import BLOB_PAYLOAD_UPDATED, BLOB_POST_SAVE


@receiver(BLOB_POST_SAVE)
# pylint: disable=unused-argument
def post_save_replication(sender, blob, **kwargs):
    """Replicate saved metadata"""
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.save(blob)

@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def payload_updated_replication(sender, blob, **kwargs):
    """Replicate payload to target volume"""
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.payload_updated(blob)

@receiver(post_delete, sender=Blob)
# pylint: disable=unused-argument
def blob_post_delete(sender, instance, **kwargs):
    """Delete target blob"""
    # TODO: Run as task
    replication_component = instance.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.delete(instance)
