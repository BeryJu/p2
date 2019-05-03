"""p2 Serve URLs"""
from django.urls import path, register_converter

from p2.serve.converters import EverythingConverter
from p2.serve.views import ServeView

register_converter(EverythingConverter, 'everything')

app_name = 'p2_serve'
urlpatterns = [
    path('<everything:path>', ServeView.as_view(), name='access'),
]
