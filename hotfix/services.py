from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone


def send_verification_email(user_email):
    send_mail(
        "You have just received a verification email!",
        "Do not do anything",
        "annaosipchik03@gmail.com",
        [user_email],
        fail_silently=False,
    )

