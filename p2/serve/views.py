"""p2 Serve Views"""
from django.http import Http404, HttpResponse
from django.views import View

from p2.core.constants import ATTR_BLOB_HEADERS, ATTR_BLOB_MIME
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.serve.models import ServeRule


class ServeView(View):
    """View to directly access Blob"""

    def dispatch(self, request, path):
        for rule in ServeRule.objects.all():
            if rule.regex.match(path):
                lookup_key, lookup_value = rule.blob_query.split('=')
                lookup_value = lookup_value % {
                    'path': path
                }
                blob = get_object_for_user_or_404(request.user, 'p2_core.view_blob', **{
                    lookup_key: lookup_value
                })
                request.log(
                    blob_pk=blob.pk,
                    rule_pk=rule.pk)
                mime_type = blob.attributes.get(ATTR_BLOB_MIME, 'text/plain')
                headers = blob.attributes.get(ATTR_BLOB_HEADERS, {})
                response = HttpResponse(blob.payload,
                                        content_type=mime_type)
                for header_key, header_value in headers.items():
                    if header_key == 'Location':
                        response.status_code = 302
                    response[header_key] = header_value
                return response
        raise Http404
