import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_lesson.settings')

app = Celery('django_lesson')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-upcoming-lessons': {
        'task': 'lessons.tasks.check_upcoming_lessons',
        'schedule': crontab(minute='*/5'),  # каждые 5 минут
    },
}