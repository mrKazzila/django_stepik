from os import environ

# celery
CELERY_BROKER_URL = f"redis://{environ['REDIS_HOST']}:{environ['REDIS_PORT']}"
CELERY_RESULT_BACKEND = f"redis://{environ['REDIS_HOST']}:{environ['REDIS_PORT']}"
