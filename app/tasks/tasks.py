from uuid import UUID
from pydantic import EmailStr
from jinja2 import Environment, FileSystemLoader

from app.smtp.service import EmailService
from app.tasks.celery_app import celery
from app.bookings.dao import BookingDAO
from app.database import sync_session_maker


@celery.task
def send_booking_confirmation_email(
    booking_id: int,
    email_to: EmailStr,
):
    with sync_session_maker() as session:
        hotel_info = BookingDAO.find_hotel_info_by_booking_id_sync(
            session, booking_id,
        )
        data = {
            "hotel_name": hotel_info["hotel_name"],
            "room_name": hotel_info["room_name"],
            "total_cost": hotel_info["total_cost"],
            "total_days": hotel_info["total_days"]
        }
        env = Environment(loader=FileSystemLoader("app/templates/smtp/"))
        template = env.get_template("booking_confirmation_template.html")
        email_message = template.render(data)
        email_subject = "Подтверждение бронирования"
        email = EmailService.create_email(
            email_to, email_subject, email_message,
        )
        EmailService.send_mail(email)


@celery.task
def send_user_confirm_code(email_to: EmailStr, code: UUID):
    data = {"confirmation_code": code}
    env = Environment(loader=FileSystemLoader("app/templates/smtp/"))
    template = env.get_template("user_confirmation_code.html")
    email_message = template.render(data)
    email_subject = "Подтверждение регистрации"
    email = EmailService.create_email(
        email_to, email_subject, email_message,
    )
    EmailService.send_mail(email)
