"""Volume Views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionListMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.core.forms import VolumeForm
from p2.core.models import Volume


class VolumeListView(PermissionListMixin, ListView):
    """List all volumes a user can use"""

    model = Volume
    permission_required = 'p2_core.view_volume'
    ordering = 'name'

class VolumeCreateView(SuccessMessageMixin, DjangoPermissionListMixin, CreateView):
    """Create new volume"""

    # TODO: Set permission for request.user

    model = Volume
    form_class = VolumeForm
    permission_required = 'p2_core.add_volume'
    template_name = 'generic/form.html'
    success_message = _('Successfully created Volume')

    def get_success_url(self):
        return reverse('p2_ui:core-volume-list', kwargs={'volume_uuid': self.object.volume.pk})

class VolumeUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing volume"""

    model = Volume
    form_class = VolumeForm
    permission_required = 'p2_core.update_volume'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Volume')

    def get_success_url(self):
        return reverse('p2_ui:core-volume-list', kwargs={'volume_uuid': self.object.volume.pk})

class VolumeDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete volume"""

    model = Volume
    permission_required = 'p2_core.delete_volume'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted Volume')

    def get_success_url(self):
        return reverse('p2_ui:core-volume-list', kwargs={'volume_uuid': self.object.volume.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
