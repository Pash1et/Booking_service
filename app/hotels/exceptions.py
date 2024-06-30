from fastapi import status

from app.exceptions import BaseException


class HotelsLocationNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotels with this location parameters not found"


class HotelIdNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotel with this hotel_id parameter not found"
