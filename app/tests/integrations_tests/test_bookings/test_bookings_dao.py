from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    booking = await BookingDAO.add(
        user_id=1,
        room_id=1,
        date_from=datetime.strptime("2023-09-21", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-09-25", "%Y-%m-%d"),
    )

    assert booking.user_id == 1
    assert booking.room_id == 1

    booking = await BookingDAO.find_by_id(booking.id)

    assert booking is not None
