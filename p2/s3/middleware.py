"""p2 s3 routing middleware"""

# pylint: disable=too-few-public-methods
class S3RoutingMiddleware:
    """Handle request as S3 request if X-Amz-Date Header is set"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_X_AMZ_DATE' in request.META:
            request.urlconf = 'p2.s3.urls'
        response = self.get_response(request)
        return response
