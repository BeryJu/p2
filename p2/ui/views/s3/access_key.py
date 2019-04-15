"""s3 access-key views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionListMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.s3.forms import S3AccessKeyForm
# from p2.core.forms import S3AccessKeyForm
# from p2.core.models import S3AccessKey, Volume
from p2.s3.models import S3AccessKey


class S3AccessKeyListView(PermissionListMixin, ListView):
    """List all access keys the user has access to"""

    model = S3AccessKey
    permission_required = 'p2_s3.view_s3accesskey'
    ordering = 'name'

class S3AccessKeyCreateView(SuccessMessageMixin, DjangoPermissionListMixin, CreateView):
    """Create new access key"""

    # TODO: add permissions for request.user

    model = S3AccessKey
    form_class = S3AccessKeyForm
    permission_required = 'p2_s3.add_s3accesskey'
    template_name = 'generic/form.html'
    success_message = _('Successfully created S3AccessKey')

    def get_success_url(self):
        return reverse('p2_ui:core-access-key-list', kwargs={'pk': self.object.volume.pk})

class S3AccessKeyUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing access key"""

    model = S3AccessKey
    form_class = S3AccessKeyForm
    permission_required = 'p2_s3.update_s3accesskey'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated S3AccessKey')

    def get_success_url(self):
        return reverse('p2_ui:core-access-key-list', kwargs={'pk': self.object.volume.pk})

class S3AccessKeyDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete access key"""

    model = S3AccessKey
    permission_required = 'p2_s3.delete_s3accesskey'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted S3AccessKey')

    def get_success_url(self):
        return reverse('p2_ui:core-access-key-list', kwargs={'pk': self.object.volume.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
