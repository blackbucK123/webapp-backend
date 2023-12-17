from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
   retreive_slots
)
from app.server.models.slot import (
    ErrorResponseModel,
    ResponseModel,
    SlotSchema
)

router = APIRouter()

@router.get("/", response_description="Slots retrieved")
async def get_slots():
    slots = await retreive_slots()
    if slots:
        return ResponseModel(slots, "Slots data retrieved successfully")
    return ResponseModel(slots, "Empty list returned")
