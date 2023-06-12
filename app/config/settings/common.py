from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Https setting for prod
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.getenv('DJANGO_DEBUG', False)
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')

if not DEBUG:
    DOMAIN_NAME = os.environ['DOMAIN_NAME']
else:
    DOMAIN_NAME = 'http://127.0.0.1:8000/'

# Application definition
INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_extensions',

    # The following oauth apps are required:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    # Debug apps
    'debug_toolbar',

    # my_apps
    'common',
    'products.apps.ProductsConfig',
    'users.apps.UsersConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Debug middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

                # my context_processors
                'products.context_processors.baskets',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = 'var/www/static'
STATICFILES_DIRS = (BASE_DIR / '../static',)

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = 'var/www/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# users
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1
