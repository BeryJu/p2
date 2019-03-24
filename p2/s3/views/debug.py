from pprint import pprint

from django.http import HttpResponse
from django.views import View


class DebugView(View):

    def dispatch(self, request, *args, **kwargs):
        pprint(request.META)
        print(request)
        print(args)
        print(kwargs)
        return HttpResponse()
