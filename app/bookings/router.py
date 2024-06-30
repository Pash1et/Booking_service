from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings import schemas as sh
from app.bookings.dao import BookingDAO
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
    return await BookingDAO.add_one(
        session,
        user_id=current_user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
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
    booking = await BookingDAO.find_one_or_none(
        session, id=booking_id, user_id=current_user.id
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    await BookingDAO.delete_one(session, booking_id)
    return {"detail": "Success"}
