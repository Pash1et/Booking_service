from decimal import Decimal
from sqlalchemy import DECIMAL, JSON, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int]
    image_id: Mapped[int]
