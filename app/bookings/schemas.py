from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: Decimal
    total_days: int
    total_cost: int
    image_id: int
    name: str
    description: str
    services: list


class SBookingCreate(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: Decimal
    total_days: int
    total_cost: int
