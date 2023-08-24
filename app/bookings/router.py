from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.bookings import exceptions
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SGetBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(
    user: Annotated[Users, Depends(get_current_user)]
) -> list[SGetBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    user: Annotated[Users, Depends(get_current_user)],
    room_id: int,
    date_from: date,
    date_to: date,
) -> SBooking:
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise exceptions.AllRoomsOccupiedException
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_booking(
    booking_id: int,
    user: Annotated[Users, Depends(get_current_user)],
):
    return await BookingDAO.del_one(booking_id, user.id)
