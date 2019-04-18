"""p2 upload views"""
from logging import getLogger
from typing import Tuple

from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.models import Blob, Volume

LOGGER = getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LegacyObjectView(View):
    """Legacy Upload (for gyazo-based clients)"""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Main upload handler. Fully gyazo compatible."""
        if 'id' in request.POST and 'imagedata' in request.FILES:
            blob = self.handle_post_file(request.FILES['imagedata'])
            # Generate url for client to open
            # TODO: Implement this, integrate with p2.serve?
            # upload_prop = CONFIG.get('default_return_view').replace('view_', '')
            # upload_hash = getattr(upload, upload_prop, 'sha256')
            # url = reverse(CONFIG.get('default_return_view'), kwargs={'file_hash': upload_hash})
            # full_url = urljoin(CONFIG.get('external_url'), url)
            return HttpResponse(blob.uuid.hex)
        return HttpResponse(status=400)

    def handle_post_file(self, post_file) -> Tuple[Blob, bool]:
        """Handle upload of a single file, computes hashes and returns existing Upload instance and
        False as tuple if file was uploaded already.
        Otherwise, new Upload instance is created and returned in a tuple with True."""
        # Find volume which is default for legacy uploads
        volumes = get_objects_for_user(self.request.user, 'use_volume', Volume).filter(
            **{'tags__legacy-default.volume.p2.io': True}
        )
        if not volumes.exists():
            raise Http404
        # To prevent empty blobs, make sure we seek back to the beginning of our file
        post_file.seek(0)
        blob = Blob.objects.create(
            path=post_file.name,
            volume=volumes.first(),
            payload=post_file.read()
        )
        # assign permission to blob
        assign_perm('view_blob', self.request.user, blob)
        return blob
