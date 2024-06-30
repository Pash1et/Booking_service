from fastapi import status

from app.exceptions import BaseException


class RoomsNotFoundAtThisHotelId(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Rooms with this hotel_id parameter is not found"
