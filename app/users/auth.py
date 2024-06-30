import datetime

import jwt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.users.dao import UserDAO
from app.users.hasher import Hasher


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
):
    user = await UserDAO.find_one_or_none(session=session, email=email)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = (
        datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
