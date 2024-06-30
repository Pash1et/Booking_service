from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_session
from app.users.dao import UserDAO


def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return access_token


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(get_token)]
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credential_exception
    except jwt.InvalidTokenError:
        raise credential_exception
    user = await UserDAO.find_by_id(session=session, model_id=user_id)
    if user is None:
        raise credential_exception
    return user
