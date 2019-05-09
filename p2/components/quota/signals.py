"""p2 quota signals"""
from django.dispatch import receiver

from p2.components.quota.controller import QuotaController
from p2.core.signals import BLOB_PRE_SAVE


@receiver(BLOB_PRE_SAVE)
# pylint: disable=unused-argument
def blob_pre_save_quota(sender, blob, **kwargs):
    """Check quota before saving blob"""
    quota_component = blob.volume.component(QuotaController)
    if quota_component:
        quota_component.controller.before_save(blob)
