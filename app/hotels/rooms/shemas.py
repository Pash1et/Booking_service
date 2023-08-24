from pydantic import BaseModel


class SHotelRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int
    total_cost: int
    left_rooms: int
