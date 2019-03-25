
from django.urls import path, register_converter

from p2.access.converters import EverythingButSlashConverter
from p2.access.views import AccessView

register_converter(EverythingButSlashConverter, 'everything_but_slash')

urlpatterns = [
    path('<everything_but_slash:path>', AccessView.as_view(), name='access'),
]
