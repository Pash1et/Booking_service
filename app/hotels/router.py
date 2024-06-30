from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.hotels import exceptions as hotels_ex
from app.hotels import schemas as hotels_sh
from app.hotels.dao import HotelDAO
from app.rooms import exceptions as rooms_ex
from app.rooms import schemas as rooms_sh
from app.rooms.dao import RoomDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}", status_code=status.HTTP_200_OK)
async def get_hotels(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    location: str,
    date_from: date,
    date_to: date
) -> list[hotels_sh.SHotelList]:
    hotels = await HotelDAO.find_all(session, location, date_from, date_to)
    if not hotels:
        raise hotels_ex.HotelsLocationNotFoundException
    return hotels


@router.get("/id/{hotel_id}", status_code=status.HTTP_200_OK)
async def get_hotel_by_id(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int,
) -> hotels_sh.SHotel:
    hotel = await HotelDAO.find_by_id(session, model_id=hotel_id)
    if not hotel:
        raise hotels_ex.HotelIdNotFoundException
    return hotel


@router.get("/{hotel_id}/rooms", status_code=status.HTTP_200_OK)
async def get_hotel_rooms(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[rooms_sh.SHotelRoomsOut]:
    rooms = await RoomDAO.find_all(session, hotel_id, date_from, date_to)
    if not rooms:
        raise rooms_ex.RoomsNotFoundAtThisHotelId
    return rooms
