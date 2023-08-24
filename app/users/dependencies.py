from datetime import datetime
from typing import Annotated
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.users.dao import UsersDAO
from app.config import settings
from app.users.models import Users
from app.users import exceptions


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise exceptions.TokenMissingException
    return token


async def get_current_user(
        token: Annotated[str, Depends(get_token)]
) -> Users | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.InvalidTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise exceptions.TokenExpireException
    user_id: str = payload.get("sub")
    if not user_id:
        raise exceptions.UserisNotExistsException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise exceptions.UserisNotExistsException
    return user
