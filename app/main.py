from fastapi import FastAPI

from app.bookings.router import router as bookings_router

app = FastAPI()
app.include_router(bookings_router)
