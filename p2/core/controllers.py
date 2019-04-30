"""Base Controller, defining common methods across all controllers"""

# pylint: disable=too-few-public-methods
class Controller:
    """Base Controller, defining common methods across all controllers"""

    instance = None
    tags = {}

    form_class = ''

    def __init__(self, instance):
        super().__init__()
        self.instance = instance
        self.tags = instance.tags

    def get_required_tags(self):
        """Get a list of required tags, these tags can be used to set a
        path or to save credentials or other"""
        return []
