"""log log-adaptor views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionListMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

# from p2.log.forms import LogAdaptorForm
from p2.log.models import LogAdaptor


class LogAdaptorListView(PermissionListMixin, ListView):
    """List all access keys the user has access to"""

    model = LogAdaptor
    permission_required = 'p2_log.view_logadaptor'
    ordering = 'name'
    paginate_by = 10


class LogAdaptorCreateView(SuccessMessageMixin, DjangoPermissionListMixin, CreateView):
    """Create new access key"""

    # TODO: add permissions for request.user

    model = LogAdaptor
    # form_class = LogAdaptorForm
    permission_required = 'p2_log.add_logadaptor'
    template_name = 'generic/form.html'
    success_message = _('Successfully created LogAdaptor')

    def get_success_url(self):
        return reverse('p2_ui:log-adaptor-list', kwargs={'pk': self.object.volume.pk})


class LogAdaptorUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing access key"""

    model = LogAdaptor
    # form_class = LogAdaptorForm
    permission_required = 'p2_log.update_logadaptor'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated LogAdaptor')

    def get_success_url(self):
        return reverse('p2_ui:log-adaptor-list', kwargs={'pk': self.object.volume.pk})


class LogAdaptorDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete access key"""

    model = LogAdaptor
    permission_required = 'p2_log.delete_logadaptor'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted LogAdaptor')

    def get_success_url(self):
        return reverse('p2_ui:log-adaptor-list', kwargs={'pk': self.object.volume.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)