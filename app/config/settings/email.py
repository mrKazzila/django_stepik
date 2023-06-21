from os import environ

from .common import DEBUG

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # terminal email
else:
    EMAIL_HOST = environ['EMAIL_HOST']
    EMAIL_PORT = environ['EMAIL_PORT']
    EMAIL_HOST_USER = environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_SSL = environ['EMAIL_USE_SSL']
