"""p2 replication component tasks"""
from structlog import get_logger

from p2.components.replication.controller import ReplicationController
from p2.core.celery import CELERY_APP
from p2.core.models import Blob, Volume

LOGGER = get_logger()

@CELERY_APP.task
def replicate_metadata_update_task(source_blob_pk):
    """Run Replication-MetadataUpdate operation in worker thread"""
    blob = Blob.objects.get(pk=source_blob_pk)
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.metadata_update(blob).save()


@CELERY_APP.task
def replicate_payload_update_task(source_blob_pk):
    """Run Replication-PayloadUpdate operation in worker thread"""
    blob = Blob.objects.get(pk=source_blob_pk)
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.payload_update(blob).save()


@CELERY_APP.task
def replicate_delete_task(source_blob_pk):
    """Run Replication-Save operation in worker thread"""
    blob = Blob.objects.get(pk=source_blob_pk)
    replication_component = blob.volume.component(ReplicationController)
    if replication_component:
        replication_component.controller.delete(blob)


@CELERY_APP.task
def initial_full_replication(volume_pk):
    """Initial full replication after Component is configured"""
    source_volume = Volume.objects.get(pk=volume_pk)
    replication_component = source_volume.component(ReplicationController)
    assert replication_component, "ReplicationController not configured"
    replication_component.controller.full_replication(source_volume)
