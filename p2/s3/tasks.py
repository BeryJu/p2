"""p2 S3 Tasks"""
from logging import getLogger
from shutil import copyfileobj
from xml.etree import ElementTree

from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import IntegerField
from django.db.models.functions import Cast
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.celery import CELERY_APP
from p2.core.constants import ATTR_BLOB_HASH_MD5
from p2.core.exceptions import BlobException
from p2.core.models import Blob, Volume
from p2.s3.constants import (TAG_S3_MULTIPART_BLOB_PART,
                             TAG_S3_MULTIPART_BLOB_TARGET_BLOB,
                             TAG_S3_MULTIPART_BLOB_UPLOAD_ID, XML_NAMESPACE)

LOGGER = getLogger(__name__)

@CELERY_APP.task
def complete_multipart_upload(upload_id, user_pk, volume_pk, path):
    """Generator to merge all part-blobs together. Yields spaces while merging
    is running to keep request from timing out"""
    LOGGER.debug("Assembling blob '%s'", path)
    user = User.objects.get(pk=user_pk)
    volume = Volume.objects.get(pk=volume_pk)
    # Create the destination blob
    blobs = get_objects_for_user(user, 'p2_core.change_blob', Blob).filter(
        path=path, volume=volume)
    if not blobs.exists():
        LOGGER.debug("Creating new Blob")
        destination_blob = Blob.objects.create(
            path=path,
            volume=volume)
        # We're creating a new blob, hence assign all default permissions
        for permission in ['view_blob', 'change_blob', 'delete_blob']:
            assign_perm('p2_core.%s' % permission,
                        user, destination_blob)
    else:
        destination_blob = blobs.first()
        LOGGER.debug("Updating existing blob %s", destination_blob.uuid.hex)
    # Go through all temporary blobs and combine them into one
    try:
        parts = get_objects_for_user(user, 'p2_core.change_blob').filter(**{
            'tags__%s' % TAG_S3_MULTIPART_BLOB_TARGET_BLOB: path,
            'tags__%s' % TAG_S3_MULTIPART_BLOB_UPLOAD_ID: upload_id,
        })
        # We need to annotate TAG_S3_MULTIPART_BLOB_PART so we can use order_by
        parts = parts.annotate(
            part_number=Cast(KeyTextTransform(
                TAG_S3_MULTIPART_BLOB_PART, 'tags'), IntegerField())).order_by('part_number')
        LOGGER.debug("Found %d parts", len(parts))
        for index, part in enumerate(parts):
            LOGGER.debug("Appending part %d", index)
            copyfileobj(part, destination_blob)
        LOGGER.debug("Saving final blob")
        destination_blob.save()
        LOGGER.debug("Deleting parts")
        parts.delete()
    except BlobException as exc:
        return str(exc)
    root = ElementTree.Element(
        "{%s}CompleteMultipartUploadResult" % XML_NAMESPACE)
    ElementTree.SubElement(root, "Location").text = ""
    ElementTree.SubElement(root, "Bucket").text = volume.name
    ElementTree.SubElement(root, "Key").text = path
    ElementTree.SubElement(root, "ETag").text = \
        destination_blob.attributes.get(ATTR_BLOB_HASH_MD5)
    return ElementTree.tostring(root).decode('utf-8')
