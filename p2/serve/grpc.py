"""Serve GRPC functionality"""
from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from guardian.shortcuts import get_anonymous_user, get_objects_for_user

from p2.core.constants import ATTR_BLOB_HEADERS
from p2.grpc.protos.serve_pb2 import ServeReply, ServeRequest
from p2.grpc.protos.serve_pb2_grpc import ServeServicer
from p2.serve.models import ServeRule

LOGGER = getLogger(__name__)


class Serve(ServeServicer):
    """GRPC Service for Serve Application"""

    def rule_lookup(self, request: ServeRequest, rule):
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

    def get_blob_from_rule(self, request: ServeRequest):
        """Try to lookup blob from ServeRule, raise Http404 if none found"""
        for rule in ServeRule.objects.all():
            LOGGER.debug("Trying rule %s", rule.name)
            if rule.matches(request):
                LOGGER.debug("Rule %s matched", rule)
                lookups, messages = self.rule_lookup(request, rule)
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

    def RetrieveFile(self, request: ServeRequest, context):
        blob = self.get_blob_from_rule(request)
        if not blob:
            return ServeReply(
                matching=False,
                data=b'',
                headers=[])
        # request.log(blob_pk=blob.pk)
        # Since we don't use any extra views or URLs here, we don't have to
        # trick SecurityMiddleware into not returning a 302
        headers = blob.attributes.get(ATTR_BLOB_HEADERS, {})
        return ServeReply(
            matching=True,
            data=blob.read(),
            headers=headers)
