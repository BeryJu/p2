"""p2 s3 routing middleware"""

from p2.lib.config import CONFIG


# pylint: disable=too-few-public-methods
class S3RoutingMiddleware:
    """Handle request as S3 request if X-Amz-Date Header is set"""

    def __init__(self, get_response):
        self.get_response = get_response
        self._s3_base = '.' + CONFIG.y('s3.base_domain')

    def extract_host_header(self, request):
        """Extract bucket name from Host Header"""
        host_header = request.META['HTTP_HOST']
        # Make sure we remove the port suffix, if any
        if ':' in host_header:
            host_header, _ = host_header.split(':')
        if host_header.endswith(self._s3_base):
            bucket = host_header.replace(self._s3_base, '')
            return bucket
        return False

    def is_aws_request(self, request):
        """Return true if AWS-s3-style request"""
        if 'HTTP_X_AMZ_DATE' in request.META:
            return True
        if 'HTTP_AUTHORIZATION' in request.META:
            return request.META['HTTP_AUTHORIZATION'].startswith('AWS')
        return False

    def __call__(self, request):
        bucket = self.extract_host_header(request)
        if self.is_aws_request(request) or bucket:
            # Check if Host header ends with s3.base_domain, if so extract bucket from Host
            request.urlconf = 'p2.s3.explicit_urls'
            if bucket:
                # If bucket was taken from URL, we need to set it as kwarg
                request.path = '/' + bucket + request.path
                request.path_info = '/' + bucket + request.path_info
        response = self.get_response(request)
        return response
