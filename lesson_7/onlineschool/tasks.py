from celery import shared_task
from django.core.mail import EmailMessage
from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_task(subject, message, to_email=None):
    if not to_email:
        to_email = EMAIL_HOST_USER
    mail = EmailMessage(subject, message, to=[to_email])
    return mail.send()
