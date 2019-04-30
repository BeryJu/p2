"""p2 quota constants"""
from django.utils.translation import gettext_lazy as _

ACTION_NOTHING = 'nothing'
ACTION_BLOCK = 'block'
ACTION_EMAIL = 'e-mail'
ACTIONS = (
    (ACTION_NOTHING, _('Do nothing, just show warning in UI.')),
    (ACTION_BLOCK, _('Prevent further uploads to this volume.')),
    (ACTION_EMAIL, _('Send E-Mail to uploader and admin.')),
)

TAG_QUOTA_THRESHOLD = 'component.p2.io/quota/threshold'
TAG_QUOTA_ACTION = 'component.p2.io/quota/action'
