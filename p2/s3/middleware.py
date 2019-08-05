"""p2 s3 routing middleware"""
from django.contrib.auth.signals import user_logged_in
from django.http import HttpRequest
from structlog import get_logger

from p2.lib.config import CONFIG
from p2.s3.auth.aws_v4 import AWSV4Authentication
from p2.s3.errors import AWSError, AWSIncompleteBody, AWSMissingContentLength
from p2.s3.http import AWSErrorView

LOGGER = get_logger()
CONTENT_LENGTH_HEADER = 'CONTENT_LENGTH'

# pylint: disable=too-few-public-methods
class S3RoutingMiddleware:
    """Handle request as S3 request if X-Amz-Date Header is set"""

    def __init__(self, get_response):
        self.get_response = get_response
        self._s3_base = '.' + CONFIG.y('s3.base_domain')

    def process_exception(self, request: HttpRequest, exception):
        """Catch AWS-specific exceptions and show them as XML response"""
        if CONFIG.y('debug'):
            LOGGER.exception(exception)
            LOGGER.debug("Request Body ", body=request.body)
        if isinstance(exception, AWSError):
            return AWSErrorView(exception)
        return None

    def extract_host_header(self, request: HttpRequest):
        """Extract bucket name from Host Header"""
        host_header = request.META.get('HTTP_HOST', '')
        # Make sure we remove the port suffix, if any
        if ':' in host_header:
            host_header, _ = host_header.split(':')
        if host_header.endswith(self._s3_base):
            bucket = host_header.replace(self._s3_base, '')
            return bucket
        return False

    def is_aws_request(self, request: HttpRequest):
        """Return true if AWS-s3-style request"""
        if 'HTTP_X_AMZ_DATE' in request.META:
            return True
        if 'HTTP_AUTHORIZATION' in request.META:
            return request.META['HTTP_AUTHORIZATION'].startswith('AWS')
        if 'X-Amz-Signature' in request.GET:
            return True
        return False

    def check_content_length(self, request):
        """Validate Content-Length Header (is required for PUT requests)"""
        if request.method != 'PUT':
            return
        if CONTENT_LENGTH_HEADER not in request.META and request.method == 'PUT':
            raise AWSMissingContentLength
        theirs = request.META.get(CONTENT_LENGTH_HEADER)
        if theirs == '':
            raise AWSError
        theirs_int = int(theirs)
        ours = len(request.body)
        if theirs_int < 0:
            raise AWSError
        if ours < theirs_int:
            raise AWSIncompleteBody

    def __call__(self, request: HttpRequest):
        bucket = self.extract_host_header(request)
        if self.is_aws_request(request) or bucket:
            # Check if Host header ends with s3.base_domain, if so extract bucket from Host
            request.urlconf = 'p2.s3.explicit_urls'
            if bucket:
                # If bucket was taken from URL, we need to set it as kwarg
                request.path = '/' + bucket + request.path
                request.path_info = '/' + bucket + request.path_info
            try:
                self.check_content_length(request)
                # Check AWS Authentication
                if AWSV4Authentication.can_handle(request):
                    handler = AWSV4Authentication(request)
                    user = handler.validate()
                    request.user = user
                    # since we don't use django's auth.login, we
                    # send the signal ourselves
                    # this also updates user.last_login
                    user_logged_in.send(sender=self, request=request, user=user)
            except AWSError as exc:
                return self.process_exception(request, exc)
            # AWS Views don't have CSRF Tokens, hence we use csrf_exempt
            setattr(request, '_dont_enforce_csrf_checks', True)
            # GET and HEAD requests are allowed over http, everything else is redirect to https
            if request.method in ['GET', 'HEAD']:
                # Set SECURE_PROXY_SSL_HEADER so SecurityMiddleware doesn't return a 302
                request.META['HTTP_X_FORWARDED_PROTO'] = 'https'
        response = self.get_response(request)
        if CONFIG.y('debug') and response.status_code > 300:
            if response['Content-Type'] == 'text/xml':
                LOGGER.debug("Request Body", body=request.body)
                LOGGER.debug("Response Body", body=response.content)
        return response
