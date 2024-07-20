from fastapi import status

from app.exceptions import BaseException


class HotelsLocationNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отели не найдены."


class HotelIdNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден."
