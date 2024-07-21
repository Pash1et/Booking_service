from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.rooms.models import Room


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        booked_rooms = (
            select(Booking.room_id)
            .outerjoin(Room, Booking.room_id == Room.id)
            .where(
                (Room.hotel_id == hotel_id) & (
                    (
                        (Booking.date_from >= date_from) &
                        (Booking.date_from <= date_to)
                    ) | (
                        (Booking.date_from <= date_from) &
                        (Booking.date_to >= date_from)
                    )
                )
            )
        ).cte("booked_rooms")

        get_rooms = (
            select(
                Room.__table__.columns,
                ((date_to - date_from).days * Room.price).label("total_cost"),
                (Room.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).outerjoin(booked_rooms, Room.id == booked_rooms.c.room_id)
            .where(Room.hotel_id == hotel_id)
            .group_by(Room.id, booked_rooms.c.room_id)
        )

        rooms = await session.execute(get_rooms)
        return rooms.mappings().all()
