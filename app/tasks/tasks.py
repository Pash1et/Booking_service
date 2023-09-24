import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_template import create_booking_confirm_template


@celery.task
def send_booking_confirm_email(booking: dict, email_to: EmailStr):
    msg = create_booking_confirm_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
