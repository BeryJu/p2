"""Blob Views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionListMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.core.forms import BlobForm
from p2.core.models import Blob, Volume


class BlobListView(PermissionListMixin, ListView):
    """List all blobs a user has access to"""

    model = Blob
    permission_required = 'p2_core.view_blob'
    ordering = 'path'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(volume=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["volume"] = Volume.objects.get(pk=self.kwargs.get('pk'))
        return context


class BlobCreateView(SuccessMessageMixin, DjangoPermissionListMixin, CreateView):
    """Create new blob"""

    # TODO: Assing permission after creation

    model = Blob
    form_class = BlobForm
    permission_required = 'p2_core.add_blob'
    template_name = 'generic/form.html'
    success_message = _('Successfully created Blob')

    def get_success_url(self):
        return reverse('p2_ui:core-blob-list', kwargs={'pk': self.object.volume.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.payload = form.cleaned_data.get('payload').read()
        self.object.save()
        return response

class BlobUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update blob"""

    model = Blob
    form_class = BlobForm
    permission_required = 'p2_core.update_blob'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Blob')

    def get_success_url(self):
        return reverse('p2_ui:core-blob-list', kwargs={'pk': self.object.volume.pk})

    # def get_form(self):
    #     form = super().get_form()
    #     bytes_file = BytesIO(self.object.payload)
    #     form.data['payload'] = InMemoryUploadedFile(
    #         bytes_file,
    #         'payload',
    #         self.object.path,
    #         self.object.attributes.get('mime'),
    #         self.object.attributes.get('size:bytes'),
    #         'utf8')
    #     return form

class BlobDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete blob"""

    model = Blob
    permission_required = 'p2_core.delete_blob'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted Blob')

    def get_success_url(self):
        return reverse('p2_ui:core-blob-list', kwargs={'pk': self.object.volume.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
