from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirm_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Подтвердите бронирование</h1>
        Вы забронировали отель {booking["total_days"]} дней
        за {booking["total_cost"]} рублей
        """,
        subtype="html",
    )
    return email
