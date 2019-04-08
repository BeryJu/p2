from p2.log.adaptor import LOG_ADAPTOR


class StartRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOG_ADAPTOR.start_request(request)
        response = self.get_response(request)
        return response


class EndRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        LOG_ADAPTOR.end_request(request)
        return response
