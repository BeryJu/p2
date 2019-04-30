"""p2 core component"""

from p2.core.controllers import Controller


# pylint: disable=too-few-public-methods
class ComponentController(Controller):
    """Base Component Controller"""

    volume = None

    template_name = ''

    def __init__(self, instance):
        super().__init__(instance)
        self.volume = self.instance.volume
