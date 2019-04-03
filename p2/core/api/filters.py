"""core filters"""
from django_filters import FilterSet, ModelChoiceFilter

from p2.core.models import Blob, Volume


class BlobFilter(FilterSet):
    """Filter for Blob, allows filtering by Volume"""

    volume = ModelChoiceFilter(queryset=Volume.objects.all())

    class Meta:
        model = Blob
        fields = {
            'path': ['exact', 'icontains'],
            'uuid': ['exact', 'icontains'],
            'volume': ['exact'],
        }
