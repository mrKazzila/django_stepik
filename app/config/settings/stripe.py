import os

from .common import DEBUG

# stripe
STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY'] if not DEBUG else os.environ['DEBUG_STRIPE_PUBLIC_KEY']
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY'] if not DEBUG else os.environ['DEBUG_STRIPE_SECRET_KEY']
STRIPE_WEBHOOK_SECRET = os.environ['STRIPE_WEBHOOK_SECRET'] if not DEBUG else os.environ['DEBUG_STRIPE_WEBHOOK_SECRET']
