import codecs
import csv
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/import",
    tags=["Import"]
)

CSV = {
    "hotel": Hotel,
    "room": Room,
}


@router.post("")
async def import_scv(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    table_name: str,
    file: UploadFile = File(...),
):
    table_name = table_name.lower()
    table_data = []
    scvReader = csv.DictReader(
        codecs.iterdecode(file.file, "utf-8"),
        delimiter=";"
    )

    match table_name:
        case "hotel":
            for data in scvReader:
                data["services"] = data["services"].split(",")
                data["rooms_quantity"] = int(data["rooms_quantity"])
                data["image_id"] = int(data["image_id"])
                table_data.append(data)
        case "room":
            for data in scvReader:
                data["hotel_id"] = int(data["hotel_id"])
                data["services"] = data["services"].split(",")
                data["price"] = int(data["price"])
                data["quantity"] = int(data["quantity"])
                data["image_id"] = int(data["image_id"])
                table_data.append(data)
        case _:
            return {"message": f"Не удалось найти талицу с названием {table_name}."}

    result = await session.execute(
        insert(CSV[table_name]).returning(CSV[table_name]),
        table_data
    )
    await session.commit()
    return result.scalars().all()
