from datetime import date

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code,booking_count",
    [
        (5, "2024-01-01", "2024-01-05", status.HTTP_200_OK, 3),
        (5, "2024-01-01", "2024-01-05", status.HTTP_200_OK, 4),
        (5, "2024-01-01", "2024-01-05", status.HTTP_200_OK, 5),
        (5, "2024-01-01", "2024-01-05", status.HTTP_200_OK, 6),
        (5, "2024-01-01", "2024-01-05", status.HTTP_409_CONFLICT, 6),
        (5, "2024-01-01", "2024-01-05", status.HTTP_409_CONFLICT, 6),
    ],
)
async def test_add_and_get_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    status_code: status,
    booking_count: int,
    auth_async_client: AsyncClient,
):
    response = await auth_async_client.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response = await auth_async_client.get("/bookings")

    assert len(response.json()) == booking_count
