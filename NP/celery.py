import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NP.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'weekly-send-posts-monday-8am': {
        'task': 'newsportal.tasks.weekly-send-posts',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),  # Каждый понедельник в 8:00
    },
}