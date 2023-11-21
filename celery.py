from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('LENZ-API')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-photos': {
        'task': 'photo.tasks.delete_expired_photos',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}