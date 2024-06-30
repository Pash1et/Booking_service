from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings import exceptions as ex
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.rooms.models import Room


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add_one(
        cls,
        session: AsyncSession,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        booked_rooms = select(Booking).where(
            (Booking.room_id == room_id) & (
                (
                    (Booking.date_from >= date_from) &
                    (Booking.date_from <= date_to)
                ) | (
                    (Booking.date_from <= date_from) &
                    (Booking.date_to > date_from)
                )
            )
        ).cte("booked_rooms")

        get_quantity_available_rooms = (
            select(
                (Room.quantity - func.count(booked_rooms.c.user_id))
                .label("rooms_left")
            )
            .outerjoin(booked_rooms, booked_rooms.c.room_id == Room.id)
            .where(Room.id == room_id)
            .group_by(Room.quantity)
        )

        result = await session.execute(get_quantity_available_rooms)
        available_rooms = result.scalar()

        if not available_rooms:
            raise ex.RoomCanNotBooked

        get_price = select(Room.price).where(Room.id == room_id)
        price = await session.scalar(get_price)
        return await super().add_one(
            session,
            user_id=user_id,
            room_id=room_id,
            date_from=date_from,
            date_to=date_to,
            price=price,
        )

    @classmethod
    async def find_all(cls, session: AsyncSession, user_id: int):
        get_bookings = (
            select(
                Booking.__table__.columns,
                Room.image_id,
                Room.name,
                Room.description,
                Room.services,
            ).outerjoin(Room, Booking.room_id == Room.id)
            .where(Booking.user_id == user_id)
        )
        bookings = await session.execute(get_bookings)
        return bookings.mappings().all()
