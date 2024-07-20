from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.dao import BookingDAO
from app.rooms.dao import RoomDAO
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import User
from app.bookings import exceptions as ex


class BookingService:
    @classmethod
    async def delete_booking(
        cls,
        session: AsyncSession,
        current_user: User,
        booking_id: int,
    ):
        booking = await BookingDAO.find_one_or_none(
            session, id=booking_id, user_id=current_user.id
        )
        if not booking:
            raise ex.BookingNotFound
        await BookingDAO.delete_one(session, booking_id)

    @classmethod
    async def add_booking(
        cls,
        session: AsyncSession,
        current_user: User,
        date_from: date,
        date_to: date,
        room_id: int,
    ):
        room = await RoomDAO.find_by_id(session, room_id)
        if not room:
            raise ex.RoomNotFound
        new_booking = await BookingDAO.add_one(
            session,
            user_id=current_user.id,
            room_id=room_id,
            date_from=date_from,
            date_to=date_to,
        )
        send_booking_confirmation_email.delay(
            new_booking.id, current_user.email,
        )
        return new_booking
