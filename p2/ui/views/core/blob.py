"""Blob Views"""
from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import (DeleteView, DetailView, TemplateView,
                                  UpdateView)
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import (get_objects_for_user, get_perms_for_model,
                                get_users_with_perms)

from p2.core.forms import BlobForm
from p2.core.models import Blob
from p2.lib.shortcuts import get_object_for_user_or_404


class FileBrowserView(LoginRequiredMixin, TemplateView):
    """List all blobs a user has access to"""

    template_name = 'p2_core/blob_list.html'
    model = Blob

    def build_prefix_list(self, prefix, volume, add_up_prefix=True):
        """Create list of all prefixes"""
        # Create separate list of all prefixes which should be displayed
        relative_prefix_list = []
        # If prefix is deeper than /, we add a .. prefix to go up
        if prefix != '/' and add_up_prefix:
            parent_prefix = '/'.join(prefix.split('/')[:-1])
            # parent_prefix can't be blank, so we fall back to slash
            if parent_prefix == '':
                parent_prefix = '/'
            relative_prefix_list.append({
                'absolute_prefix': parent_prefix,
                'relative_prefix': '..'
            })
        for blob in get_objects_for_user(self.request.user, 'p2_core.view_blob').filter(
                volume=volume,
                prefix__startswith=prefix).distinct('prefix'):
            # To prevent the absolute path being //x, replace prefix with ''
            if prefix == '/':
                prefix = ''
            relative = blob.prefix.replace(prefix, '', 1)
            if '/' in relative and relative != '' and relative != '/':
                next_part = relative.split('/')[1]
                relative_prefix_list.append({
                    'absolute_prefix': '/'.join([prefix, next_part]),
                    'relative_prefix': next_part
                })
        return relative_prefix_list

    def build_breadcrumb_list(self, prefix):
        """Build list for breadcrumbs"""
        until_here = []
        crumbs = []
        for part in prefix.split('/'):
            if part == '':
                continue
            until_here.append(part)
            crumbs.append({
                'title': part,
                'prefix': '/'.join(until_here)
            })
        return crumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['volume'] = get_object_for_user_or_404(
            self.request.user, 'p2_core.use_volume', pk=self.kwargs.get('pk'))

        # Get list of blobs with matching prefix
        prefix = self.request.GET.get('prefix', '/')
        blobs = get_objects_for_user(self.request.user, 'p2_core.view_blob').filter(
            prefix=prefix,
            volume=context['volume']).order_by('path')

        context['prefixes'] = self.build_prefix_list(prefix, context['volume'])
        context['breadcrumbs'] = self.build_breadcrumb_list(prefix)

        # If we have more than 20 prefixes, we don't need to lookup objects
        if len(context['prefixes']) > 20 or not context['prefixes']:
            page = self.request.GET.get('page', 1)
            objects_per_page = 20
            if page == 1:
                objects_per_page = 20 - len(context['prefixes'])

            paginator = Paginator(blobs, objects_per_page)
            context['objects'] = paginator.get_page(page)

        return context

class BlobDetailView(PermissionRequiredMixin, DetailView):
    """View Blob Details"""

    model = Blob
    permission_required = 'p2_core.view_blob'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = FileBrowserView().build_breadcrumb_list(self.object.prefix)
        context['users_perms'] = OrderedDict(
            sorted(
                get_users_with_perms(self.object, attach_perms=True,
                                     with_group_users=False).items(),
                key=lambda user: user[0].username
            )
        )
        context['model_perms'] = get_perms_for_model(self.object.__class__)
        return context

class BlobUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update blob"""

    model = Blob
    form_class = BlobForm
    permission_required = 'p2_core.change_blob'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Blob')

    def get_success_url(self):
        return reverse('p2_ui:core-blob-list', kwargs={'pk': self.object.volume.pk})


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


class BlobDownloadView(PermissionRequiredMixin, DetailView):
    """Download blob's payload"""

    model = Blob
    permission_required = 'p2_core.view_blob'

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        response = HttpResponse(
            self.object, content_type=self.object.attributes.get('mime', 'text/plain'))
        response['Content-Disposition'] = 'attachment; filename=' + self.object.path
        return response
