import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotfix.settings")
app = Celery("hotfix")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.user_schedule = {
    "check-users-every-day":
        {
            'task': 'users.tasks.delete_users', 'schedule': crontab(hour='*/24')
        },
}