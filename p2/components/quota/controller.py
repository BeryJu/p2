"""p2 quota controller"""

from p2.components.quota.constants import TAG_QUOTA_THRESHOLD
from p2.core.components.base import ComponentController


# pylint: disable=too-few-public-methods
class QuotaController(ComponentController):
    """Quota controller"""

    template_name = 'components/quota/card.html'
    form_class = 'p2.components.quota.forms.QuotaForm'

    # TODO: Implement core functionality

    @property
    def threshold(self):
        """Get threshold"""
        return int(self.instance.tags.get(TAG_QUOTA_THRESHOLD, 0))

    @property
    def quota_percentage(self):
        """Check if volume is close to any quota"""
        threshold = int(self.instance.tags.get(TAG_QUOTA_THRESHOLD, 0))
        if threshold == 0:
            return 0
        return self.volume.space_used / (threshold / 100)
