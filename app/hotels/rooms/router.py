from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.shemas import SHotelRooms

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> list[SHotelRooms]:
    return await RoomsDAO.find_all(hotel_id, date_from, date_to)
