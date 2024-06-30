from fastapi import status

from app.exceptions import BaseException


class NotFoundUserException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"


class UserAleadyExistException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this Email already exists"
