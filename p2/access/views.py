from re import compile

from django.shortcuts import get_object_or_404
from django.views import View
from guardian.shortcuts import get_objects_for_user

from p2.access.models import AccessRule
from p2.core.models import Blob


class AccessView(View):

    def dispatch(self, request, path):
        for rule in AccessRule.objects.all():
            if rule.regex.matches(path):
                lookup_key, lookup_value = rule.blob_query.split('=')
                lookup_value = lookup_value % {
                    'path': path
                }
                blob = get_object_or_404(Blob, **{lookup_key: lookup_value})
                if request.user.has_perm('p2_core.view_blob', blob):
                    # TODO: Show blob
                    print('we did it')
