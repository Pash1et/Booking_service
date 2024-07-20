from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.hotels import exceptions as hotels_ex
from app.hotels.dao import HotelDAO
from app.rooms import exceptions as rooms_ex
from app.rooms.dao import RoomDAO


class HotelService:
    @classmethod
    async def get_hotels_by_location(
        cls,
        session: AsyncSession,
        location: str,
        date_from: date,
        date_to: date
    ):
        hotels = await HotelDAO.find_by_location_and_date(
            session, location, date_from, date_to,
        )
        if not hotels:
            raise hotels_ex.HotelsLocationNotFoundException
        return hotels

    @classmethod
    async def get_hotel_by_id(
        cls, session: AsyncSession, hotel_id: int,
    ):
        hotel = await HotelDAO.find_by_id(session, model_id=hotel_id)
        if not hotel:
            raise hotels_ex.HotelIdNotFoundException
        return hotel

    @classmethod
    async def get_hotel_rooms(
        cls, session, hotel_id, date_from, date_to,
    ):
        rooms = await RoomDAO.find_all(session, hotel_id, date_from, date_to)
        if not rooms:
            raise rooms_ex.RoomsNotFoundAtThisHotelId
        return rooms
