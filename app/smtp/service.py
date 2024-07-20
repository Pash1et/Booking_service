from email.message import EmailMessage
import smtplib

from pydantic import EmailStr

from app.config import settings


class EmailService:
    @classmethod
    def create_email(cls, reciver_email: EmailStr, subject: str, message: str):
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = settings.SMTP_USER
        email["To"] = reciver_email
        email.set_content(message, subtype="html")
        return email

    @classmethod
    def send_mail(cls, email: EmailMessage):
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(email)
