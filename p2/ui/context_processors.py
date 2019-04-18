"""p2 UI Context Processors"""

from p2 import __version__


def version(request):
    """return version number"""
    return {
        'p2_version': __version__
    }
