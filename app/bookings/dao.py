from datetime import date

from sqlalchemy import and_, func, insert, or_, select, delete

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker
from app.bookings import exceptions


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            booking_query = (
                select(
                    cls.model.__table__.columns,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services
                )
                .where(cls.model.user_id == user_id)
                .join(Rooms, cls.model.room_id == Rooms.id, isouter=True)
            )
            users_bookings = await session.execute(booking_query)
            return users_bookings.mappings().all()

    @classmethod
    async def del_one(cls, bookind_id: int, user_id: int):
        async with async_session_maker() as session:
            booking_query = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.id == bookind_id,
                        Bookings.user_id == user_id)
                    )
            )
            booking = await session.execute(booking_query)
            if booking.first() is None:
                raise exceptions.BookingNotFoundException
            delete_query = (
                delete(Bookings)
                .where(
                    and_(
                        Bookings.id == bookind_id,
                        Bookings.user_id == user_id
                    )
                )
            )
            await session.execute(delete_query)
            await session.commit()

    @classmethod
    async def add(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        booked_rooms = select(cls.model).where(
            and_(
                cls.model.room_id == room_id,
                or_(
                    and_(
                        cls.model.date_from >= date_from,
                        cls.model.date_from <= date_to
                    ),
                    and_(
                        cls.model.date_from <= date_from,
                        cls.model.date_to > date_from
                    )
                )
            )
        ).cte("booked_rooms")

        rooms_left = (
            select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms")
            )
            .select_from(Rooms)
            .join(
                booked_rooms,
                booked_rooms.c.room_id == Rooms.id,
                isouter=True
            )
            .where(
                Rooms.id == room_id
            )
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        async with async_session_maker() as session:
            result = await session.execute(rooms_left)
            rooms: int = result.scalar()

            if rooms == 0:
                return None

            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price: int = price.scalar()
            add_booking = insert(cls.model).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(cls.model)
            booking = await session.execute(add_booking)
            await session.commit()
            return booking.scalar_one()
