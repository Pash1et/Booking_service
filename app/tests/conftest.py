import pytest

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.bookings.models import Bookings
from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


@pytest.fixture(autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)
