from datetime import date
from decimal import Decimal

from sqlalchemy import DECIMAL, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[Decimal] = mapped_column(DECIMAL)
    total_days: Mapped[int] = mapped_column(
        Integer, Computed("date_to - date_from")
    )
    total_cost: Mapped[int] = mapped_column(
        Integer, Computed("(date_to - date_from) * price")
    )
