"""p2 Serve Views"""
from logging import getLogger

from django.http import Http404
from django.views import View
from guardian.shortcuts import get_objects_for_user

from p2.core.constants import ATTR_BLOB_HEADERS
from p2.core.http import BlobResponse
from p2.serve.models import ServeRule

LOGGER = getLogger(__name__)


class ServeView(View):
    """View to directly access Blob"""

    def rule_lookup(self, rule, path):
        """Build blob lookup from rule"""
        lookups = {}
        debug_messages = []
        for lookup_token in rule.blob_query.split('&'):
            debug_messages.append("Found new token '%s'" % lookup_token)
            lookup_key, lookup_value = lookup_token.split('=')
            lookups[lookup_key] = lookup_value % {
                'path': path
            }
            debug_messages.append("Formatted to '%s'" % lookups[lookup_key])
        debug_messages.append("Final lookup %r" % lookups)
        return lookups, debug_messages

    def dispatch(self, request, path):
        for rule in ServeRule.objects.all():
            if rule.regex.match(path):
                LOGGER.debug("Rule %s matched", rule)
                lookups, messages = self.rule_lookup(rule, path)
                # Output debug messages on log
                for msg in messages:
                    LOGGER.debug(msg)
                blobs = get_objects_for_user(
                    self.request.user, 'p2_core.view_blob').filter(**lookups)
                if not blobs.exists():
                    LOGGER.debug("No blob found matching ")
                    continue
                blob = blobs.first()
                request.log(
                    blob_pk=blob.pk,
                    rule_pk=rule.pk)
                headers = blob.attributes.get(ATTR_BLOB_HEADERS, {})
                response = BlobResponse(blob)
                for header_key, header_value in headers.items():
                    if header_key == 'Location':
                        response.status_code = 302
                    response[header_key] = header_value
                return response
        raise Http404
