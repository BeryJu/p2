"""p2 s3 URL converters"""

from django.urls.converters import StringConverter


class S3BucketConverter(StringConverter):
    """Match S3 bucket regex"""

    regex = '([a-z]|(d(?!d{0,2}.d{1,3}.d{1,3}.d{1,3})))([a-zd]|(.(?!(.|-)))|(-(?!.))){1,61}[a-zd.]'

class EverythingConverter(StringConverter):
    """Match Everything. Just used for debugging"""

    regex = '.*'
