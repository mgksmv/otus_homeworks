import time
from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_task(subject, message, to_email=None):
    if not to_email:
        to_email = EMAIL_HOST_USER
    return send_mail(subject, message, EMAIL_HOST_USER, [to_email], fail_silently=False)
