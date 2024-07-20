from typing import Type

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from app.database import Base


class BaseDAO:
    model: Type[Base] = None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add_one(cls, session: AsyncSession, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar()

    @classmethod
    async def update_one(cls, session: AsyncSession, model_id: int, **data):
        query = (
            update(cls.model)
            .where(cls.model.id == model_id)
            .values(**data)
            .returning(cls.model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar()

    @classmethod
    async def delete_one(cls, session: AsyncSession, model_id: int):
        query = delete(cls.model).where(cls.model.id == model_id)
        await session.execute(query)
        await session.commit()

    @classmethod
    def find_by_id_sync(cls, session: Session, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = session.execute(query)
        return result.scalar_one_or_none()
