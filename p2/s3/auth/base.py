"""p2 s3 base authentication"""

class BaseAuth:
    """Base Authentication class"""

    request = None

    def __init__(self, request):
        self.request = request

    @staticmethod
    def can_handle(request):
        """Return True if this class can handle request"""
        raise NotImplementedError

    def validate(self):
        """Return a tuple of User, None if authentication was
        successful or None, ErrorCode if not"""
        raise NotImplementedError
