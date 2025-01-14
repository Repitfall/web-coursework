from django.core.mail import send_mail
from celery import shared_task


@shared_task
def mail_send(recipient_email, subject, message):
    send_mail(subject, message, 'noreply@example.com', [recipient_email], fail_silently=False)
    return "Письмо отправлено!"

