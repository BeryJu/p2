"""p2 Logging middleware"""
from p2.log.adaptor import LOG_ADAPTOR


# pylint: disable=too-few-public-methods
class StartRequestMiddleware:
    """Initialize Logging as early as possible"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOG_ADAPTOR.start_request(request)
        response = self.get_response(request)
        return response


# pylint: disable=too-few-public-methods
class EndRequestMiddleware:
    """Finish logging of request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        LOG_ADAPTOR.end_request(request)
        return response
