"""Replication signals"""

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from p2.components.replication.constants import TAG_REPLICATION_OFFSET
from p2.components.replication.controller import ReplicationController
from p2.components.replication.tasks import (initial_full_replication,
                                             replicate_delete_task,
                                             replicate_metadata_update_task,
                                             replicate_payload_update_task)
from p2.core.models import Blob, Component
from p2.core.signals import BLOB_PAYLOAD_UPDATED, BLOB_POST_SAVE
from p2.lib.reflection import class_to_path


@receiver(BLOB_POST_SAVE)
# pylint: disable=unused-argument
def post_save_replication(sender, blob, **kwargs):
    """Replicate saved metadata"""
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replicate_metadata_update_task.apply_async(
            (blob.pk,),
            countdown=int(replication_component.tags.get(TAG_REPLICATION_OFFSET, 0)))


@receiver(BLOB_PAYLOAD_UPDATED)
# pylint: disable=unused-argument
def payload_updated_replication(sender, blob, **kwargs):
    """Replicate payload to target volume"""
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replicate_payload_update_task.apply_async(
            (blob.pk,),
            countdown=int(replication_component.tags.get(TAG_REPLICATION_OFFSET, 0)))


@receiver(pre_delete, sender=Blob)
# pylint: disable=unused-argument
def blob_pre_delete(sender, instance, **kwargs):
    """Delete target blob"""
    replication_component = instance.volume.component(ReplicationController)
    if replication_component:
        replicate_delete_task.apply_async(
            (instance.pk,),
            countdown=int(replication_component.tags.get(TAG_REPLICATION_OFFSET, 0)))


@receiver(post_save, sender=Component)
# pylint: disable=unused-argument
def component_post_save(sender, instance, **kwargs):
    """Trigger initial sync after we've been saved"""
    if instance.controller_path == class_to_path(ReplicationController):
        initial_full_replication.delay(instance.volume.pk)
