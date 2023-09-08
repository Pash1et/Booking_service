from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.bookings.router import router as router_bookings
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.users.router import router as router_users

from app.config import settings

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
