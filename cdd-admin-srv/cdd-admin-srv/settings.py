import os
import logging
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'logs/cdd-admin-srv.log')
STATS_FILE = os.path.join(BASE_DIR, 'logs/cdd-admin-srv.log')

DEBUG = True
USE_TZ = False
USE_I18N = True
USE_L10N = True
ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
ROOT_URLCONF = 'cdd-admin-srv.urls'
WSGI_APPLICATION = 'cdd-admin-srv.wsgi.application'
SECRET_KEY = '+c@9pvo%4f9g0k7oy=8gmv$jo=6vg)=flid9h$w*8996d!hp@4'

# ====================
# = Logging Settings =
# ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)-12s] %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'log_stats': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': STATS_FILE,
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        # 'sentry': {
        #     'level': 'ERROR',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'cdd': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'stats': {
            'handlers': ['console', 'log_stats'],
            'level': 'INFO',
            'propagate': False,
        },
        'commands': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
}

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=24 * 60 * 60)
}

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'rest_framework_swagger',
    'rest_framework',
    'django_filters',
    'corsheaders',

    'apps.account',
    'apps.user',
    'apps.promotion',
    'apps.lottery',
    'apps.finance',
    'apps.order',
    'apps.pay',
    'apps.analysis',
    'apps.config',
    'apps.event',
    'apps.upload',
    'apps.admin'
]
STATIC_URL = '/static/'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': True
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

LOGIN_URL = 'http://localhost:8080/login'
LOGOUT_URL = 'http://localhost:8080/logout'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'apps.exception.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.account.auth.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

AUTHENTICATION_BACKENDS = [
    'apps.account.auth.backends.CommerceAuthenticationBackend',
    'apps.account.auth.backends.ProxyAuthenticationBackend',
    'apps.account.auth.backends.ChannelAuthenticationBackend'
]

DATABASE_ROUTERS = ['apps.routers.DBRouter']

try:
    if os.getenv('ENV') == 'pro':
        from production_settings import *    # NOQA
    elif os.getenv('ENV') == 'stg':
        from staging_settings import *       # NOQA
    else:
        from local_settings import *         # NOQA
except ImportError:
    pass
