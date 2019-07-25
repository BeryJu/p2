"""Serve GRPC functionality"""
from logging import getLogger
from typing import List, Match, Optional, Tuple

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from guardian.shortcuts import get_anonymous_user, get_objects_for_user

from p2.core.constants import TAG_BLOB_HEADERS
from p2.core.models import Blob
from p2.grpc.protos.serve_pb2 import ServeReply, ServeRequest
from p2.grpc.protos.serve_pb2_grpc import ServeServicer
from p2.log.adaptor import LOG_ADAPTOR
from p2.serve.models import ServeRule

LOGGER = getLogger(__name__)

# pylint: disable=too-few-public-methods
class MockRequest:
    """Dumb class we use to emulate a Django HTTP Request"""

    uid = None
    user = None
    path = None
    META = {}

    def __init__(self, request: ServeRequest):
        for header, value in request.headers.items():
            self.META[header] = value

    def log(self, **kwargs):
        """Stub for p2.log's request logger"""
        pass

class Serve(ServeServicer):
    """GRPC Service for Serve Application"""

    def rule_lookup(self, request: ServeRequest, rule: ServeRule,
                    match: Match) -> Tuple[List[str], List[str]]:
        """Build blob lookup from rule"""
        lookups = {}
        # FIXME: Capture LOGGER output instead of returning a message array
        debug_messages = []
        for lookup_token in rule.blob_query.split('&'):
            debug_messages.append("Found new token '%s'" % lookup_token)
            lookup_key, lookup_value = lookup_token.split('=')
            lookups[lookup_key] = lookup_value.format(
                path=request.url,
                path_relative=request.url[1:],
                host=request.headers.get('Host', ''),
                meta=request.headers,
                match=match,
            )
            debug_messages.append("Formatted to '%s'='%s'" % (lookup_key, lookups[lookup_key]))
        debug_messages.append("Final lookup %r" % lookups)
        return lookups, debug_messages

    def get_user(self, request: ServeRequest) -> User:
        """Get user from cookie"""
        session = Session.objects.filter(session_key=request.session)
        if not session.exists():
            return get_anonymous_user()
        uid = session.first().get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return user

    def get_blob_from_rule(self, request: ServeRequest) -> Optional[Blob]:
        """Try to lookup blob from ServeRule, raise Http404 if none found"""
        for rule in ServeRule.objects.all():
            LOGGER.debug("Trying rule %s", rule.name)
            regex_match = rule.matches(request)
            if regex_match:
                LOGGER.debug("Rule %s matched", rule)
                lookups, messages = self.rule_lookup(request, rule, regex_match)
                # Output debug messages on log
                for msg in messages:
                    LOGGER.debug(msg)
                blobs = get_objects_for_user(
                    self.get_user(request), 'p2_core.view_blob').filter(**lookups)
                if not blobs.exists():
                    LOGGER.debug("No blob found matching ")
                    continue
                return blobs.first()
        return None

    def RetrieveFile(self, request: ServeRequest, context) -> ServeReply:
        mock_request = MockRequest(request)
        mock_request.user = self.get_user(request)
        mock_request.path = request.url
        LOG_ADAPTOR.start_request(mock_request)
        blob = self.get_blob_from_rule(request)
        LOG_ADAPTOR.end_request(mock_request)
        if not blob:
            return ServeReply(
                matching=False,
                data=b'',
                headers={
                    "X-p2-Request-Id": mock_request.uid
                })
        mock_request.log(blob_pk=blob.pk)
        # Since we don't use any extra views or URLs here, we don't have to
        # trick SecurityMiddleware into not returning a 302
        headers = blob.tags.get(TAG_BLOB_HEADERS, {})
        headers["X-p2-Request-Id"] = mock_request.uid
        return ServeReply(
            matching=True,
            data=blob.read(),
            headers=headers)
