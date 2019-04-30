"""Storage Views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.core.forms import StorageForm
from p2.core.models import Storage


class StorageListView(PermissionListMixin, ListView):
    """List all storages a user can use"""

    model = Storage
    permission_required = 'p2_core.view_storage'
    ordering = 'name'
    paginate_by = 10


class StorageCreateView(SuccessMessageMixin, DjangoPermissionRequiredMixin, CreateView):
    """Create new storage"""

    # TODO: Set permission for request.user

    model = Storage
    form_class = StorageForm
    permission_required = 'p2_core.add_storage'
    template_name = 'generic/form.html'
    success_message = _('Successfully created Storage')

    def get_success_url(self):
        return reverse('p2_ui:core-storage-list')


class StorageUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing storage"""

    model = Storage
    form_class = StorageForm
    permission_required = 'p2_core.update_storage'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Storage')

    def get_success_url(self):
        return reverse('p2_ui:core-storage-list')


class StorageDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete storage"""

    model = Storage
    permission_required = 'p2_core.delete_storage'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted Storage')

    def get_success_url(self):
        return reverse('p2_ui:core-storage-list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
