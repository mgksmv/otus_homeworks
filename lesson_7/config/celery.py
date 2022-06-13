import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

onlineschool_app = Celery('onlineschool')
onlineschool_app.config_from_object('django.conf:settings', namespace='CELERY')
onlineschool_app.autodiscover_tasks()
