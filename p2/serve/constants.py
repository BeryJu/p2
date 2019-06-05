"""p2 server constants"""

# Matches full Request Path, starting with leading slash
TAG_SERVE_MATCH_PATH = 'serve.p2.io/match/path'
# Matches relative Request Path, without leading slash
TAG_SERVE_MATCH_PATH_RELATIVE = 'serve.p2.io/match/path/relative'
# Matches request Hostname
TAG_SERVE_MATCH_HOST = 'serve.p2.io/match/host'
# Match any Header mentioned here
# https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.META
# e.g. serve.p2.io/match/meta/HTTP_USER_AGENT
TAG_SERVE_MATCH_META = 'serve.p2.io/match/meta/'
