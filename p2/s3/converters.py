"""p2 s3 URL converters"""

from django.urls.converters import StringConverter


class S3BucketConverter(StringConverter):
    """Match S3 bucket regex"""

    regex = r'([a-zA-Z0-9\-_]+)'

class EverythingConverter(StringConverter):
    """Match Everything. Just used for debugging"""

    regex = '.*'
