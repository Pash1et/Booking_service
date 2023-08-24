from fastapi import status

from app.exceptions import CustomException


class UsersException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserAlreadyExistsException(UsersException):
    detail = "User already exists"


class IncorrectEmailOrPasswordException(UsersException):
    detail = "Wrong email or password"


class TokenMissingException(UsersException):
    detail = "Token is missing"


class InvalidTokenFormatException(UsersException):
    detail = "Invalid token format"


class TokenExpireException(UsersException):
    detail = "Token has been expired"


class UserisNotExistsException(UsersException):
    pass
