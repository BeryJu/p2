"""
Django settings for p2 project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import datetime
import logging
import os
import socket
import sys
from urllib.parse import urlparse

import ldap
from django_auth_ldap.config import LDAPSearch

from p2 import __version__
from p2.lib.config import CONFIG

LOGGER = logging.getLogger(__name__)


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('secret_key',
                        '48e9z8tw=_z0e#m*x70&)u%cgo8#=16uzdze&i8q=*#**)@cp&')  # noqa Debug

DEBUG = CONFIG.get('debug')
CORS_ORIGIN_ALLOW_ALL = DEBUG

# config's external_url is a full URL, so we have to parse it to get the host
# Also allow server's hostname and server's fqdn
ALLOWED_HOSTS = set([
    urlparse(CONFIG.get('external_url')).netloc,
    socket.getfqdn(),
    socket.gethostname()
] + CONFIG.get('domains', []))

INTERNAL_IPS = ['127.0.0.1']

# Redis settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s" % CONFIG.get('redis'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_CACHE_ALIAS = "default"

# Celery settings
# Add a 10 minute timeout to all Celery tasks.
CELERY_TASK_SOFT_TIME_LIMIT = 600
CELERY_BEAT_SCHEDULE = {}
CELERY_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = 'p2'
CELERY_BROKER_URL = 'redis://%s' % CONFIG.get('redis')
CELERY_RESULT_BACKEND = 'redis://%s' % CONFIG.get('redis')
CELERY_IMPORTS = ('p2.core.tasks', )

# Influxdb settings
# with CONFIG.cd('influx'):
#     INFLUXDB_DISABLED = not CONFIG.get('enabled')
#     INFLUXDB_HOST = CONFIG.get('host')
#     INFLUXDB_PORT = CONFIG.get('port')
#     INFLUXDB_USER = CONFIG.get('user')
#     INFLUXDB_PASSWORD = CONFIG.get('password')
#     INFLUXDB_DATABASE = CONFIG.get('database')
#     INFLUXDB_TIMEOUT = 5
#     INFLUXDB_USE_CELERY = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# LDAP Settings
with CONFIG.cd('ldap'):
    if CONFIG.get('enabled'):
        AUTH_LDAP_SERVER_URI = CONFIG.get('server').get('uri')
        AUTH_LDAP_START_TLS = CONFIG.get('server').get('tls')
        AUTH_LDAP_BIND_DN = CONFIG.get('bind').get('dn')
        AUTH_LDAP_BIND_PASSWORD = CONFIG.get('bind').get('password')
        # pylint: disable=no-member
        AUTH_LDAP_USER_SEARCH = LDAPSearch(CONFIG.get('search_base'),
                                           ldap.SCOPE_SUBTREE, CONFIG.get('filter'))
        AUTHENTICATION_BACKENDS += [
            'django_auth_ldap.backend.LDAPBackend',
        ]
        if CONFIG.get('require_group'):
            AUTH_LDAP_REQUIRE_GROUP = CONFIG.get('require_group')

ACCOUNT_EMAIL_VERIFICATION = 'none'

with CONFIG.cd('web'):
    CHERRYPY_SERVER = {
        'server.socket_host': CONFIG.get('listen', '0.0.0.0'),  # nosec
        'server.socket_port': CONFIG.get('port', 8000),
        'server.thread_pool': CONFIG.get('threads', 30),
        'log.screen': False,
        'log.access_file': '',
        'log.error_file': '',
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',
    'p2.core.apps.P2CoreConfig',
    'p2.api.apps.P2APIConfig',
    'p2.s3.apps.P2S3Config',
    'p2.serve.apps.P2ServeConfig',
    'p2.image.apps.P2ImageConfig',
    # API Frameworks
    'rest_framework',
    'drf_yasg',
    'django_filters'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'p2.root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'p2/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

VERSION = __version__

WSGI_APPLICATION = 'p2.root.wsgi.application'

DATA_UPLOAD_MAX_MEMORY_SIZE = 536870912

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}
for db_alias, db_config in CONFIG.get('databases').items():
    DATABASES[db_alias] = {
        'ENGINE': db_config.get('engine'),
        'HOST': db_config.get('host'),
        'NAME': db_config.get('name'),
        'USER': db_config.get('user'),
        'PASSWORD': db_config.get('password'),
        'OPTIONS': db_config.get('options', {}),
    }

with CONFIG.cd('email'):
    EMAIL_HOST = CONFIG.get('host', default='localhost')
    EMAIL_PORT = CONFIG.get('port', default=25)
    EMAIL_HOST_USER = CONFIG.get('user', default='')
    EMAIL_HOST_PASSWORD = CONFIG.get('password', default='')
    EMAIL_USE_TLS = CONFIG.get('use_tls', default=False)
    EMAIL_USE_SSL = CONFIG.get('use_ssl', default=False)
    EMAIL_FROM = CONFIG.get('from')
    SERVER_EMAIL = CONFIG.get('from')

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# RAVEN_CONFIG = {
#     'dsn': 'https://dfcc6acbd9c543ea8d4c9dbf4ac9a8c0:5340ca78902841b5b'
#            '3372ecce5d548a5@sentry.services.beryju.org/4',
#     'release': VERSION,
#     'environment': 'production' if DEBUG is False else 'development',
#     'tags': {'site': CONFIG.get('external_url')}
# }

# ERROR_REPORT_ENABLED = CONFIG.get('error_report_enabled', False)
# if not ERROR_REPORT_ENABLED:
#     RAVEN_CONFIG['dsn'] = ''

# API Configurations

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'p2.api.urls.INFO',
    'SECURITY_DEFINITIONS': {
        'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_guardian.filters.DjangoObjectPermissionsFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'p2.api.permissions.CustomObjectPermissions',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    # ),
}


with CONFIG.cd('log'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': ('%(asctime)s %(levelname)-8s %(name)-55s '
                           '%(funcName)-20s %(message)s'),
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': ('%(log_color)s%(asctime)s %(levelname)-8s %(name)-55s '
                           '%(funcName)-20s %(message)s'),
            }
        },
        'handlers': {
            'console': {
                'level': CONFIG.get('level').get('console'),
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            },
            'file': {
                'level': CONFIG.get('level').get('file'),
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': CONFIG.get('file'),
            },
        },
        'loggers': {
            'p2': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'allauth': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'cherrypy': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'celery': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
                'propagate': True,
            },
            'django_auth_ldap': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'botocore': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }


TEST = any('test' in arg for arg in sys.argv)
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = 2

TEST_OUTPUT_FILE_NAME = 'unittest.xml'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

if TEST:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
    }
    CELERY_TASK_ALWAYS_EAGER = True

if DEBUG is True:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
