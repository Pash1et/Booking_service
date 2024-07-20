from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_async_engine(settings.database_url)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession,
                                   expire_on_commit=False)

sync_engine = create_engine(settings.database_url_sync)
sync_session_maker = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
