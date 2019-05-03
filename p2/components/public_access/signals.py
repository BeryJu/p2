"""public Access signals"""

from django.dispatch import receiver

from p2.components.public_access.controller import PublicAccessController
from p2.core.signals import BLOB_POST_SAVE


@receiver(BLOB_POST_SAVE)
# pylint: disable=unused-argument
def blob_post_save_perms(sender, blob, **kwargs):
    """Assign Permissions for Anonymous User"""
    public_access_component = blob.volume.component(PublicAccessController)
    if public_access_component:
        public_access_component.controller.add_permissions(blob)
