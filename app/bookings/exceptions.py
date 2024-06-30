from fastapi import status

from app.exceptions import BaseException


class RoomCanNotBooked(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет свободных номеров."
