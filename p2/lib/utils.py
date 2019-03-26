"""p2 generic utils"""

from base64 import b64encode


def url_b64encode(input_str):
    """Convert string to URL-Friendly base64"""
    return b64encode(input_str.encode('utf-8'), b'_-').decode('utf-8')
