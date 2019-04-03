"""p2 generic utils"""
import socket
from base64 import b64encode

from django.http import HttpRequest


def url_b64encode(input_str):
    """Convert string to URL-Friendly base64"""
    return b64encode(input_str.encode('utf-8'), b'_-').decode('utf-8')


def get_remote_ip(request: HttpRequest) -> str:
    """Return the remote's IP"""
    if not request:
        return '0.0.0.0'
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        return request.META.get('HTTP_X_FORWARDED_FOR')
    return request.META.get('REMOTE_ADDR')


def get_reverse_dns(ipaddress: str) -> str:
    """Does a reverse DNS lookup and returns the first IP"""
    try:
        rev = socket.gethostbyaddr(ipaddress)
        if rev:
            return rev[0]
        return ''  # noqa
    except (socket.herror, socket.gaierror, TypeError, IndexError):
        return ''
