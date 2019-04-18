"""p2 UI Index view"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from guardian.shortcuts import get_objects_for_user

from p2.core.models import Blob


class IndexView(LoginRequiredMixin, TemplateView):
    """Show overview of volumes"""

    template_name = 'general/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['count'] = len(Blob.objects.all())
        data['volumes'] = get_objects_for_user(self.request.user, 'p2_core.view_volume')
        return data
