"""serve rule views"""
from django.contrib import messages
from django.contrib.auth.mixins import \
    PermissionRequiredMixin as DjangoPermissionListMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from p2.serve.forms import ServeRuleForm
from p2.serve.models import ServeRule


class ServeRuleListView(PermissionListMixin, ListView):
    """List all serve rules the user has access to"""

    model = ServeRule
    permission_required = 'p2_serve.view_serverule'
    ordering = 'name'
    paginate_by = 10


class ServeRuleCreateView(SuccessMessageMixin, DjangoPermissionListMixin, CreateView):
    """Create new serve rule"""

    # TODO: add permissions for request.user

    model = ServeRule
    form_class = ServeRuleForm
    permission_required = 'p2_serve.add_serverule'
    template_name = 'generic/form.html'
    success_message = _('Successfully created Rule')

    def get_success_url(self):
        return reverse('p2_ui:serve-rule-list', kwargs={'pk': self.object.volume.pk})


class ServeRuleUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Update existing serve rule"""

    model = ServeRule
    form_class = ServeRuleForm
    permission_required = 'p2_serve.update_serverule'
    template_name = 'generic/form.html'
    success_message = _('Successfully updated Rule')

    def get_success_url(self):
        return reverse('p2_ui:serve-rule-list', kwargs={'pk': self.object.volume.pk})


class ServeRuleDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """Delete serve rule"""

    model = ServeRule
    permission_required = 'p2_serve.delete_serverule'
    template_name = 'generic/delete.html'
    success_message = _('Successfully deleted Rule')

    def get_success_url(self):
        return reverse('p2_ui:serve-rule-list', kwargs={'pk': self.object.volume.pk})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
