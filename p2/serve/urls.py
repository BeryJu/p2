"""p2 Serve URLs"""
from django.urls import path, register_converter

from p2.serve.converters import EverythingButSlashConverter
from p2.serve.views import ServeView

register_converter(EverythingButSlashConverter, 'everything_but_slash')

app_name = 'p2_serve'
urlpatterns = [
    path('<everything_but_slash:path>', ServeView.as_view(), name='access'),
]
