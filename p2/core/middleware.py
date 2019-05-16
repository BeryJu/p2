"""p2 core middlewares"""

from django.http import HttpResponse


class HealthCheckMiddleware:
    """Kubernetes Healtheck middleware"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.method == "GET" and request.META['HTTP_HOST'] == 'kubernetes-healthcheck-host':
            return self.healthz(request)
        return self.get_response(request)

    def healthz(self, request):
        """Returns that the server is alive."""
        return HttpResponse("OK")
