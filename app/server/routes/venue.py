from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
   retreive_venues
)
from app.server.models.venue import (
    ErrorResponseModel,
    ResponseModel,
    VenueSchema
)

router = APIRouter()

@router.get("/", response_model=List[VenueSchema])
async def get_venues():
    try:
        venues = await retreive_venues()
        if venues:
            return venues
        else:
            return ResponseModel([], "No venues found")
    except Exception as e:
        return ErrorResponseModel(str(e), 400, "An error occurred while retrieving venues")