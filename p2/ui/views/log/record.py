"""log record views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from guardian.mixins import PermissionListMixin

from p2.log.models import LogAdaptor, Record


class RecordListView(PermissionListMixin, LoginRequiredMixin, ListView):
    """List all log records the user has access to"""

    model = Record
    permission_required = 'p2_log.view_record'
    ordering = '-start_time'
    paginate_by = 10

    def get_queryset(self):
        # TODO Filter by permission
        self.extra_context = {
            'adaptor': LogAdaptor.objects.get(pk=self.kwargs.get('pk'))
        }
        return Record.objects.filter(adaptor__pk=self.kwargs.get('pk')).order_by(self.ordering)
