"""p2 Serve Views"""
from django.http import Http404, HttpResponse
from django.views import View

from p2.core.constants import ATTR_BLOB_HEADERS, ATTR_BLOB_MIME
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.serve.models import ServeRule


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
                lookups, _ = self.rule_lookup(rule, path)
                blob = get_object_for_user_or_404(self.request.user, 'p2_core.view_blob', **lookups)
                request.log(
                    blob_pk=blob.pk,
                    rule_pk=rule.pk)
                mime_type = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
                headers = blob.attributes.get(ATTR_BLOB_HEADERS, {})
                response = HttpResponse(blob,
                                        content_type=mime_type)
                for header_key, header_value in headers.items():
                    if header_key == 'Location':
                        response.status_code = 302
                    response[header_key] = header_value
                return response
        raise Http404
