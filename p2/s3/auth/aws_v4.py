"""p2 s3 authentication mixin"""
import hashlib
import hmac
from collections import OrderedDict
from logging import getLogger
from typing import Any, List, Optional
from urllib.parse import quote

from django.contrib.auth.models import User
from django.http import HttpRequest, QueryDict

from p2.api.models import APIKey
from p2.s3.auth.base import BaseAuth
from p2.s3.errors import (AWSAccessDenied, AWSContentSignatureMismatch,
                          AWSSignatureMismatch)

LOGGER = getLogger(__name__)

class SignatureMismatch(Exception):
    """Exception raised when given Hash does not match request body's hash"""

# pylint: disable=too-many-instance-attributes
class AWSv4AuthenticationRequest:
    """Holds all pieces of an AWSv4 Authenticated Request"""

    algorithm: str = ""
    signed_headers: str = ""
    signature: str = ""
    access_key: str = ""
    date: str = ""
    date_long: str = ""
    region: str = ""
    service: str = ""
    request: str = ""
    hash: str = ""

    def __init__(self):
        self.algorithm = self.date = self.signed_headers = self.signature = self.hash = ""
        self.access_key = self.date_long = self.region = self.service = self.request = ""

    @property
    def credentials(self) -> str:
        """Join properties together to re-construct credential string"""
        return "/".join([
            self.date,
            self.region,
            self.service,
            self.request
        ])

    @credentials.setter
    def credentials(self, value: str):
        # Further split credential value
        self.access_key, self.date, self.region, self.service, self.request = value.split('/')

    @staticmethod
    def from_querystring(get_dict: QueryDict) -> Optional['AWSv4AuthenticationRequest']:
        """Check if AWSv4 Authentication information was sent via Querystring,
        abd parse it into an AWSv4AuthenticationRequest object. If querystring doesn't
        contain necessary parameters, None is returned."""
        required_parameters = ['X-Amz-Date', 'X-Amz-Credential',
                               'X-Amz-SignedHeaders', 'X-Amz-Signature']
        for required_parameter in required_parameters:
            if required_parameter not in get_dict:
                return None
        auth_request = AWSv4AuthenticationRequest()
        auth_request.credentials = get_dict.get('X-Amz-Credential')
        auth_request.signed_headers = get_dict.get('X-Amz-SignedHeaders')
        auth_request.date_long = get_dict.get('X-Amz-Date')
        auth_request.signature = get_dict.get('X-Amz-Signature')
        return auth_request

    @staticmethod
    def from_header(headers: dict) -> Optional['AWSv4AuthenticationRequest']:
        """Check if AWSv4 Authentication information was sent via headers,
        and parse it into an AWSv4AuthenticationRequest object. If headers don't
        contain necessary information, None is returned."""
        # Check if headers exist, otherwise return None
        if 'HTTP_AUTHORIZATION' not in headers:
            return None
        auth_request = AWSv4AuthenticationRequest()
        auth_request.algorithm, credential_container = \
            headers.get('HTTP_AUTHORIZATION').split(' ', 1)
        credential, signed_headers, signature = credential_container.split(',')
        # Remove "Credential=" from string
        _, auth_request.credentials = credential.split("=")
        _, auth_request.signed_headers = signed_headers.split("=")
        _, auth_request.signature = signature.split("=")
        auth_request.date_long = headers.get('HTTP_X_AMZ_DATE')
        if not auth_request.date_long:
            auth_request.date_long = auth_request.date
        return auth_request

class AWSV4Authentication(BaseAuth):
    """AWS v4 Signer"""

    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    def _sign(self, key: str, msg: str) -> hmac.HMAC:
        """Simple HMAC wrapper"""
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256)

    def _get_signature_key(self, key: str, auth_request: AWSv4AuthenticationRequest) -> str:
        """Create signature like
        https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html"""
        k_date = self._sign(('AWS4' + key).encode('utf-8'), auth_request.date).digest()
        k_region = self._sign(k_date, auth_request.region).digest()
        k_service = self._sign(k_region, auth_request.service).digest()
        k_signing = self._sign(k_service, auth_request.request).digest()
        return k_signing

    def _make_query_string(self) -> str:
        """Parse existing Querystring, URI-encode them and sort them and put them back together"""
        pairs = []
        if self.request.META['QUERY_STRING'] == '':
            return self.request.META['QUERY_STRING']
        for kv_pair in self.request.META['QUERY_STRING'].split('&'):
            if '=' not in kv_pair:
                kv_pair = kv_pair + '='
            pairs.append(kv_pair)
        pairs.sort()
        return '&'.join(pairs)

    def _get_canonical_headers(self, only: List[str]) -> str:
        """Fix header keys from HTTP_X to x"""
        canonical_headers = ""
        for header_key, header_value in OrderedDict(sorted(self.request.META.items())).items():
            fixed_key = header_key.replace('HTTP_', '', 1).replace('_', '-').lower()
            if fixed_key in only:
                canonical_headers += f"{fixed_key}:{header_value}\n"
        return canonical_headers

    def _get_sha256(self, data: Any) -> str:
        """Get body hash in sha256"""
        hasher = hashlib.sha256()
        hasher.update(data)
        return hasher.hexdigest()

    def _get_canonical_request(self, auth_request: AWSv4AuthenticationRequest) -> str:
        """Create canonical request in AWS format (
        https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html)"""
        signed_headers_keys = auth_request.signed_headers.split(';')

        canonical_request = [
            self.request.META.get('REQUEST_METHOD', ''),
            quote(self.request.META.get('PATH_INFO', '')),
            self._make_query_string(),
            self._get_canonical_headers(signed_headers_keys),
            auth_request.signed_headers,
            auth_request.hash,
        ]
        return '\n'.join(canonical_request)

    def _lookup_access_key(self, access_key: str) -> Optional[APIKey]:
        """Lookup access_key in database, return secret if found otherwise None"""
        keys = APIKey.objects.filter(access_key=access_key)
        if keys.exists():
            return keys.first()
        return None

    @staticmethod
    def can_handle(request: HttpRequest) -> bool:
        if 'HTTP_AUTHORIZATION' in request.META:
            return 'AWS4-HMAC-SHA256' in request.META['HTTP_AUTHORIZATION']
        if 'X-Amz-Signature' in request.GET:
            return True
        return False

    def validate(self) -> Optional[User]:
        """Check Authorization Header in AWS Compatible format"""
        auth_request = AWSv4AuthenticationRequest.from_header(self.request.META)
        if not auth_request:
            auth_request = AWSv4AuthenticationRequest.from_querystring(self.request.GET)
        auth_request.hash = self.request.META.get('HTTP_X_AMZ_CONTENT_SHA256')

        # Verify given Hash with request body
        if auth_request.hash != self._get_sha256(self.request.body):
            LOGGER.debug("CONTENT_SHA256 Header/param incorrect")
            raise AWSContentSignatureMismatch
        # Build our own signature to compare
        secret_key = self._lookup_access_key(auth_request.access_key)
        if not secret_key:
            LOGGER.debug("No secret key found for request %s", auth_request.access_key)
            raise AWSAccessDenied
        signing_key = self._get_signature_key(secret_key.secret_key, auth_request)
        canonical_request = self._get_canonical_request(auth_request)
        string_to_sign = '\n'.join([
            auth_request.algorithm,
            auth_request.date_long,
            auth_request.credentials,
            self._get_sha256(canonical_request.encode('utf-8')),
        ])
        our_signature = self._sign(signing_key, string_to_sign).hexdigest()
        if auth_request.signature != our_signature:
            LOGGER.debug("Canonical Request: '%s'", canonical_request)
            LOGGER.debug("Ours: %s", our_signature)
            LOGGER.debug("Theirs: %s", auth_request.signature)
            raise AWSSignatureMismatch
        return secret_key.user
