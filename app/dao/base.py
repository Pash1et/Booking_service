from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
