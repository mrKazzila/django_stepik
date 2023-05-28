import logging
import os

from celery import Celery
from django.conf import settings

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.debug(f'Request: {self.request!r}')
