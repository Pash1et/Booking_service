from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.schemas import SBooking
from app.database import get_async_session
from app.bookings.dao import BookingDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> list[SBooking]:
    return await BookingDAO.find_all(session)


@router.get("/{booking_id}")
async def get_booking(booking_id: int):
    pass
