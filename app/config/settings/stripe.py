from os import environ

from .common import DEBUG

# stripe
STRIPE_PUBLIC_KEY = environ['STRIPE_PUBLIC_KEY'] if not DEBUG else environ['DEBUG_STRIPE_PUBLIC_KEY']
STRIPE_SECRET_KEY = environ['STRIPE_SECRET_KEY'] if not DEBUG else environ['DEBUG_STRIPE_SECRET_KEY']
STRIPE_WEBHOOK_SECRET = environ['STRIPE_WEBHOOK_SECRET'] if not DEBUG else environ['DEBUG_STRIPE_WEBHOOK_SECRET']
