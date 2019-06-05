"""p2 serve routing middleware"""
import hashlib
from logging import getLogger

from django.core.cache import cache
from guardian.shortcuts import get_objects_for_user

from p2.core.constants import ATTR_BLOB_HEADERS
from p2.core.http import BlobResponse
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.serve.models import ServeRule

LOGGER = getLogger(__name__)


LOGGER = getLogger(__name__)

# pylint: disable=too-few-public-methods
class ServeRoutingMiddleware:
    """Check if request matches any ServeRules and routes it to serve URLs"""

    request = None

    def __init__(self, get_response):
        self.get_response = get_response

    def fingerprint(self):
        """Return request's fingerprint"""
        fingerprint_data = [
            self.request.path,
            str(self.request.user.pk or 0),
            str(hash(frozenset(self.request.META.items()))),
        ]
        _hash = hashlib.sha256()
        _hash.update("".join(fingerprint_data).encode('utf-8'))
        return _hash.hexdigest()

    def rule_lookup(self, rule):
        """Build blob lookup from rule"""
        lookups = {}
        # FIXME: Capture LOGGER output instead of returning a message array
        debug_messages = []
        for lookup_token in rule.blob_query.split('&'):
            debug_messages.append("Found new token '%s'" % lookup_token)
            lookup_key, lookup_value = lookup_token.split('=')
            lookups[lookup_key] = lookup_value.format(
                path=self.request.path,
                path_relative=self.request.path[1:],
                host=self.request.META.get('HTTP_HOST', ''),
                meta=self.request.META,
            )
            debug_messages.append("Formatted to '%s'='%s'" % (lookup_key, lookups[lookup_key]))
        debug_messages.append("Final lookup %r" % lookups)
        return lookups, debug_messages

    def get_blob_from_rule(self):
        """Try to lookup blob from ServeRule, raise Http404 if none found"""
        for rule in ServeRule.objects.all():
            if rule.matches(self.request):
                LOGGER.debug("Rule %s matched", rule)
                lookups, messages = self.rule_lookup(rule)
                # Output debug messages on log
                for msg in messages:
                    LOGGER.debug(msg)
                blobs = get_objects_for_user(
                    self.request.user, 'p2_core.view_blob').filter(**lookups)
                if not blobs.exists():
                    LOGGER.debug("No blob found matching ")
                    continue
                # Log rule_id for debugging
                self.request.log(rule_pk=rule.pk)
                return blobs.first()
        return None

    def __call__(self, request):
        self.request = request
        cache_key = 'p2_serve:%s' % self.fingerprint()
        # Quickly check if path exists in cache and has blob mapped to it
        cached_value = cache.get(cache_key, default=None)
        if cached_value:
            LOGGER.debug("Using Blob PK from cache")
            blob = get_object_for_user_or_404(request.user, 'p2_core.view_blob', pk=cached_value)
        else:
            blob = self.get_blob_from_rule()
            if not blob:
                response = self.get_response(request)
                return response
            # save blob pk so we don't need to re-evaluate rules
            cache.set(cache_key, blob.pk)
        request.log(blob_pk=blob.pk)
        # Since we don't use any extra views or URLs here, we don't have to
        # trick SecurityMiddleware into not returning a 302
        headers = blob.attributes.get(ATTR_BLOB_HEADERS, {})
        response = BlobResponse(blob)
        for header_key, header_value in headers.items():
            if header_key == 'Location':
                response.status_code = 302
            response[header_key] = header_value
        return response