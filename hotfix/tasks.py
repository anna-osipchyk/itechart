from datetime import timedelta

from django.utils import timezone

from users.models import Employee
from .services import send_verification_email
from .celery import app


@app.task
def send(user_email):
    send_verification_email(user_email)

@app.task
def delete_users_schedule():
    Employee.objects.filter(last_login__lt=timezone.now() - timedelta(days=365)).delete()

