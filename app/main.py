from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.importer.router import router as importer_router
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(importer_router)
