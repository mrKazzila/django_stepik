from os import getenv

from .common import BASE_DIR  # noqa

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom_formatter': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
