from fastapi import status

from app.exceptions import CustomException


class AllRoomsOccupiedException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = "All rooms are occupied"


class BookingNotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking bot found"
