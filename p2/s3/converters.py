class S3BucketConverter:

    regex = '([a-z]|(d(?!d{0,2}.d{1,3}.d{1,3}.d{1,3})))([a-zd]|(.(?!(.|-)))|(-(?!.))){1,61}[a-zd.]'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

class PathConverter:

    regex = '.*'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
