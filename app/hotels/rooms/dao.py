from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            hotel_rooms_query = (
                select(cls.model.id).where(cls.model.hotel_id == hotel_id)
            ).cte("hotel_rooms")

            booking_rooms = (
                select(Bookings).where(
                    and_(
                        Bookings.room_id.in_(hotel_rooms_query.select()),
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
            ).cte("booking_rooms")

            left_rooms = (
                select(
                    cls.model.id,
                    (cls.model.quantity - func.count(booking_rooms.c.room_id)).label(
                        "left_rooms"
                    ),
                )
                .select_from(cls.model)
                .join(
                    booking_rooms, booking_rooms.c.room_id == cls.model.id, isouter=True
                )
                .where(cls.model.id.in_(hotel_rooms_query.select()))
                .group_by(cls.model.quantity, booking_rooms.c.room_id, cls.model.id)
            ).cte("left_rooms")

            days = date_to - date_from
            rooms_query = (
                select(
                    cls.model.__table__.columns,
                    (cls.model.price * days.days).label("total_cost"),
                    left_rooms.c.left_rooms,
                )
                .join(left_rooms, left_rooms.c.id == cls.model.id)
                .where(cls.model.hotel_id == hotel_id)
            )

            rooms = await session.execute(rooms_query)
            return rooms.mappings().all()
