from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.hotels import schemas as hotels_sh
from app.hotels.dao import HotelDAO
from app.hotels.service import HotelService
from app.rooms import schemas as rooms_sh

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}", status_code=status.HTTP_200_OK)
async def get_hotels_by_location(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    location: str,
    date_from: date,
    date_to: date
) -> list[hotels_sh.SHotelList]:
    return await HotelService.get_hotels_by_location(
        session, location, date_from, date_to,
    )


@router.get("/id/{hotel_id}", status_code=status.HTTP_200_OK)
async def get_hotel_by_id(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int,
) -> hotels_sh.SHotel:
    return await HotelService.get_hotel_by_id(session, hotel_id)


@router.get("/{hotel_id}/rooms", status_code=status.HTTP_200_OK)
async def get_hotel_rooms(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[rooms_sh.SHotelRoomsOut]:
    return await HotelService.get_hotel_rooms(
        session, hotel_id, date_from, date_to
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_hotels(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[hotels_sh.SHotel]:
    return await HotelDAO.find_all(session)
