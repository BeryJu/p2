"""p2 public_access controller"""
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user
from structlog import get_logger

from p2.core.components.base import ComponentController

LOGGER = get_logger()

# pylint: disable=too-few-public-methods
class PublicAccessController(ComponentController):
    """Add permissions to blob to be publicly accessible"""

    template_name = 'components/public_access/card.html'
    # No custom form needed
    form_class = 'p2.core.components.forms.ComponentForm'

    def add_permissions(self, blob):
        """Assign permission"""
        assign_perm('p2_core.view_blob', get_anonymous_user(), blob)
