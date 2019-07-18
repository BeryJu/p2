"""p2 s3 routing middleware"""
from logging import getLogger

from p2.lib.config import CONFIG
from p2.s3.auth.aws_v4 import AWSV4Authentication
from p2.s3.http import AWSError

LOGGER = getLogger(__name__)

# pylint: disable=too-few-public-methods
class S3RoutingMiddleware:
    """Handle request as S3 request if X-Amz-Date Header is set"""

    def __init__(self, get_response):
        self.get_response = get_response
        self._s3_base = '.' + CONFIG.y('s3.base_domain')

    def extract_host_header(self, request):
        """Extract bucket name from Host Header"""
        host_header = request.META.get('HTTP_HOST', '')
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
            # Check AWS Authentication
            if AWSV4Authentication.can_handle(request):
                handler = AWSV4Authentication(request)
                user, error_code = handler.validate()
                # LOGGER.debug("Authenticated user %s", user)
                if error_code:
                    return AWSError(error_code)
                request.user = user
            # AWS Views don't have CSRF Tokens, hence we use csrf_exempt
            setattr(request, '_dont_enforce_csrf_checks', True)
            # GET and HEAD requests are allowed over http, everything else is redirect to https
            if request.method in ['GET', 'HEAD']:
                # Set SECURE_PROXY_SSL_HEADER so SecurityMiddleware doesn't return a 302
                request.META['HTTP_X_FORWARDED_PROTO'] = 'https'
        response = self.get_response(request)
        return response
