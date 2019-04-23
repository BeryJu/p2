"""p2 s3 authentication mixin"""
import hashlib
import hmac
from collections import OrderedDict
from logging import getLogger
from xml.etree import ElementTree

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from p2.s3.constants import ErrorCodes
from p2.s3.http import XMLResponse
from p2.s3.models import S3AccessKey

LOGGER = getLogger(__name__)

class S3Authentication(View):
    """Emulate S3 Authentication"""

    def error_response(self, code):
        """Return generic S3 Error response"""
        root = ElementTree.Element("Error")
        code_name, response_code = code.value
        ElementTree.SubElement(root, "Code").text = code_name
        return XMLResponse(root, status=response_code)

    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    def _sign(self, key, msg):
        """Simple HMAC wrapper"""
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def _get_signautre_key(self, key, date_stamp, region_name, service_name):
        """Create signautre like
        https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html"""
        k_date = self._sign(('AWS4' + key).encode('utf-8'), date_stamp)
        k_region = self._sign(k_date, region_name)
        k_service = self._sign(k_region, service_name)
        k_signing = self._sign(k_service, 'aws4_request')
        return k_signing

    def _make_query_string(self):
        """Parse existing Querystring, URI-encode them and sort them and put them back together"""
        paris = []
        if self.request.META['QUERY_STRING'] == '':
            return self.request.META['QUERY_STRING']
        for kv_pair in self.request.META['QUERY_STRING'].split('&'):
            if '=' not in kv_pair:
                kv_pair = kv_pair + '='
            paris.append(kv_pair)
        paris.sort()
        return '&'.join(paris)

    def _fix_header_keys(self):
        """Fix header keys from HTTP_X to x"""
        headers = {}
        for header_key, header_value in self.request.META.items():
            fixed_key = header_key.replace('HTTP_', '', 1).replace('_', '-').lower()
            headers[fixed_key] = header_value
        return OrderedDict(sorted(headers.items()))

    def _get_canonical_request(self, signed_headers):
        """Create canonical request in AWS format (
        https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html)"""
        canonical_headers = ''
        signed_headers_keys = signed_headers.split(';')
        LOGGER.debug("Headers to sign: %r", signed_headers_keys)
        # sorted_headers = OrderedDict(sorted())
        for header_key, header_value in self._fix_header_keys().items():
            if header_key in signed_headers_keys:
                canonical_headers += '%s:%s\n' % (header_key, header_value)
        canonical_request = [
            self.request.META['REQUEST_METHOD'],
            self.request.META['PATH_INFO'],
            self._make_query_string(), # self.request.META['QUERY_STRING'],
            canonical_headers,
            signed_headers,
            self.request.META['HTTP_X_AMZ_CONTENT_SHA256']
        ]
        return '\n'.join(canonical_request)

    def _lookup_access_key(self, access_key):
        """Lookup access_key in database, return secret if found otherwise None"""
        keys = S3AccessKey.objects.filter(access_key=access_key)
        if keys.exists():
            return keys.first()
        return None

    # pylint: disable=too-many-locals
    def authenticate(self):
        """Check Authorization Header in AWS Compatible format"""
        raw = self.request.META.get('HTTP_AUTHORIZATION')
        # LOGGER.debug("Raw Header: %r", raw)
        if not raw:
            return False
        algorithm, credential_container = raw.split(' ', 1)
        credential, signed_headers, signature = credential_container.split(',')
        # Remove "Credentail=" from string
        _, credential = credential.split("=")
        _, signed_headers = signed_headers.split("=")
        _, signature = signature.split("=")
        LOGGER.debug("Got from client: %s", signature)
        # Further split credential value
        access_key, date, region, service, _request = credential.split('/')
        # Build our own signature to compare
        secret_key = self._lookup_access_key(access_key)
        if not secret_key:
            return False
        signing_key = self._get_signautre_key(secret_key.secret_key, date, region, service)
        canonical_request = self._get_canonical_request(signed_headers)
        # LOGGER.debug("Canonical Request: '%s'", canonical_request)
        canonical_request_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        string_to_sign = '\n'.join([
            algorithm,
            self.request.META['HTTP_X_AMZ_DATE'],
            "%s/%s/s3/aws4_request" % (date, region),
            canonical_request_hash
        ])
        # LOGGER.debug("Signing %s", string_to_sign)
        our_signature = hmac.new(signing_key, string_to_sign.encode('utf-8'),
                                 hashlib.sha256).hexdigest()
        LOGGER.debug("We got %s", our_signature)
        if signature == our_signature:
            self.request.user = secret_key.user
            return True
        return False

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        authenticated = self.authenticate()
        if not authenticated:
            return self.error_response(ErrorCodes.ACCESS_DENIED)
        if 'redundant_slash' in kwargs:
            kwargs.pop('redundant_slash')
        return super().dispatch(request, *args, **kwargs)
