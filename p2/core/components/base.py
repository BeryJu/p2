"""p2 core component"""

# pylint: disable=too-few-public-methods
class ComponentController:
    """Base Component Controller"""

    volume = None
    component = None

    template_name = ''
    form_class = ''

    def __init__(self, component):
        self.component = component
        self.volume = component.volume
