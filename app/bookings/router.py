from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings import schemas as sh
from app.bookings.dao import BookingDAO
from app.bookings.service import BookingService
from app.database import get_async_session
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("", status_code=status.HTTP_200_OK)
async def add_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    date_from: date,
    date_to: date,
    room_id: int,
) -> sh.SBookingCreate:
    return await BookingService.add_booking(
        session,
        current_user,
        date_from,
        date_to,
        room_id,
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_curr_user_bookings(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[sh.SBooking]:
    return await BookingDAO.find_all(session, user_id=current_user.id)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    booking_id: int,
):
    return await BookingService.delete_booking(
        session,
        current_user,
        booking_id,
    )
