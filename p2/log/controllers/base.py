"""p2 log base controller"""
from p2.core.controllers import Controller


class LogController(Controller):
    """p2 log base controller"""

    form_class = 'p2.log.forms.LogAdaptorForm'

    def log(self, record_data):
        """Write log record"""
        raise NotImplementedError()
