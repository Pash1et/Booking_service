from decimal import Decimal

from pydantic import BaseModel


class SHotelRoomsOut(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list
    price: Decimal
    quantity: int
    image_id: int
    total_cost: Decimal
    rooms_left: int
