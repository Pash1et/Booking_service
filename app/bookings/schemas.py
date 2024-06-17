from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: Decimal
    total_days: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)
