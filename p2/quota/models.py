"""p2 Quota"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from p2.core.models import Volume
from p2.lib.models import UUIDModel

ACTION_NOTHING = 'nothing'
ACTION_BLOCK = 'block'
ACTION_EMAIL = 'e-mail'
ACTIONS = (
    (ACTION_NOTHING, _('Do nothing, just show warning in UI.')),
    (ACTION_BLOCK, _('Prevent further uploads to this volume.')),
    (ACTION_EMAIL, _('Send E-Mail to uploader and admin.')),
)

class Quota(UUIDModel):
    """Quota about how much storage can be used on a per-volume level"""

    name = models.TextField()
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    threshold = models.IntegerField()
    action = models.TextField(choices=ACTIONS, default=ACTION_NOTHING)

    def __str__(self):
        return "Quota of %s on Volume %s" % (self.threshold, self.volume.name)
