"""Storage Views"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.core.forms import StorageForm
from p2.core.models import Blob, Storage
from p2.lib.reflection import path_to_class
from p2.lib.views import CreateAssignPermView


class StorageListView(PermissionListMixin, LoginRequiredMixin, ListView):
    """List all storages a user can use"""

    model = Storage
    permission_required = 'p2_core.view_storage'
    ordering = 'name'
    paginate_by = 10


class StorageDetailView(PermissionRequiredMixin, DetailView):
    """Show details about storage instance"""

    model = Storage
    permission_required = 'p2_core.view_storage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_blobs'] = len(Blob.objects.filter(volume__storage=self.object))
        context['total_space'] = sum(x.space_used for x in self.object.volume_set.all())
        return context


class StorageCreateView(SuccessMessageMixin, DjangoPermissionRequiredMixin, CreateAssignPermView):
    """Create new storage"""

    model = Storage
    form_class = StorageForm
    permission_required = 'p2_core.add_storage'
    template_name = 'generic/form.html'
    success_message = _('Successfully created Storage')
    permissions = [
        'p2_core.view_storage',
        'p2_core.change_storage',
        'p2_core.delete_storage',
    ]

    def get_success_url(self):
        return reverse('p2_ui:core-storage-list')


class StorageUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing storage"""

    model = Storage
    permission_required = 'p2_core.change_storage'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Storage')

    def get_form_class(self):
        return path_to_class(self.object.controller.form_class)

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
