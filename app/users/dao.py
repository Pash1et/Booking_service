from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.users.models import ConfirmCode, User


class UserDAO(BaseDAO):
    model = User


class UserConfirmCodeDAO(BaseDAO):
    model = ConfirmCode

    @classmethod
    async def create_confirm_code(cls, session: AsyncSession, user: User):
        query = (
            insert(ConfirmCode)
            .values(user_id=user.id)
            .returning(ConfirmCode)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar()
