from fastapi import status

from app.exceptions import BaseException


class NotFoundUserException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неправильный логин или пароль."


class UserAleadyExistException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователь с этим Email уже зарегистрирован."


class UserIsNotActiavate(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Учетная запись не подтверждена."


class UserConfirmationCodeNotFound(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный код."
