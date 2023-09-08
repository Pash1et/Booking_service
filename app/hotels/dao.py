from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            bookings = (
                select(Bookings)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to
                        ),
                        and_(
                            Bookings.date_from < date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
                .subquery("filter_bookings")
            )

            hotels_rooms_left = (
                select(
                    Rooms.hotel_id,
                    (
                        cls.model.rooms_quantity
                        - func.count(bookings.c.room_id)
                    ).label("rooms_left")
                )
                .select_from(cls.model)
                .outerjoin(Rooms, Rooms.hotel_id == cls.model.id)
                .outerjoin(bookings, bookings.c.room_id == Rooms.id)
                .where(
                    cls.model.location.contains(location.title())
                )
                .group_by(cls.model.rooms_quantity, Rooms.hotel_id)
            ).cte("rooms_left")

            get_hotels = (
                select(
                    cls.model.__table__.columns,
                    hotels_rooms_left.c.rooms_left
                )
                .select_from(cls.model)
                .join(
                    hotels_rooms_left,
                    hotels_rooms_left.c.hotel_id == cls.model.id
                )
            )
            hotels = await session.execute(get_hotels)
            return hotels.mappings().all()
