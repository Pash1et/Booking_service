from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.hotels.models import Hotel
from app.rooms.models import Room


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        location: str,
        date_from: date,
        date_to: date
    ):
        booked_rooms = (
            select(Hotel, Room.hotel_id)
            .join(Room, Hotel.id == Room.hotel_id)
            .join(Booking, Room.id == Booking.room_id)
            .where(
                (Hotel.location.like(f"%{location}%")) & (
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

        get_hotels = (
            select(
                Hotel.__table__.columns,
                (Hotel.rooms_quantity - func.count(booked_rooms.c.hotel_id)).label("rooms_left")
            )
            .outerjoin(booked_rooms, Hotel.id == booked_rooms.c.hotel_id)
            .where(Hotel.location.like(f"%{location}%"))
            .group_by(Hotel.id)
            .having((Hotel.rooms_quantity - func.count(booked_rooms.c.hotel_id)) > 0)
        )

        hotels = await session.execute(get_hotels)
        return hotels.mappings().all()
