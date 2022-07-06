from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_activation_email(mail_subject, message, user_email):
    mail = EmailMessage(mail_subject, message, to=[user_email])
    return mail.send()
