from fastapi import status

from app.exceptions import BaseException


class RoomCanNotBooked(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет свободных номеров."


class RoomNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Комната не найдена."


class BookingNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Бронирование не найдено."
