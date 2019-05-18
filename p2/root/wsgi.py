"""
WSGI config for p2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os
from logging import getLogger
from time import time

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p2.core.settings")

LOGGER = getLogger(__name__)


class WSGILogger:
    """ This is the generalized WSGI middleware for any style request logging. """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        start = time()
        status_codes = []
        content_lengths = []

        def custom_start_response(status, response_headers, exc_info=None):
            status_codes.append(int(status.partition(' ')[0]))
            for name, value in response_headers:
                if name.lower() == 'content-length':
                    content_lengths.append(int(value))
                    break
            return start_response(status, response_headers, exc_info)
        retval = self.application(environ, custom_start_response)
        runtime = int((time() - start) * 10**6)
        content_length = content_lengths[0] if content_lengths else 0
        self.log(status_codes[0], environ, content_length,
                 ip_header=None, runtime=runtime)
        return retval

    def log(self, status_code, environ, content_length, **kwargs):
        """
        Apache log format 'NCSA extended/combined log':
        "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
        see http://httpd.apache.org/docs/current/mod/mod_log_config.html#formats
        """
        # Let's collect log values
        val = {}
        ip_header = kwargs.get('ip_header', None)
        if ip_header:
            val['host'] = environ.get(ip_header, '')
        else:
            val['host'] = environ.get('REMOTE_ADDR', '')
        val['request'] = "{0} {1} {2}".format(
            environ.get('REQUEST_METHOD', ''),
            environ.get('PATH_INFO', ''),
            environ.get('SERVER_PROTOCOL', '')
        )
        val['status'] = status_code
        val['size'] = content_length / 1000 if content_length > 0 else '-'
        val['runtime'] = kwargs.get('runtime')
        # see http://docs.python.org/3/library/string.html#format-string-syntax
        format_string = '%(host)s => "%(request)s" => %(status)d %(size)skB %(runtime)dms'
        LOGGER.info(format_string, val)

application = WSGILogger(get_wsgi_application())
