from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_tournaments
)
from app.server.models.tournament import (
    ErrorResponseModel,
    ResponseModel,
    TournamentSchema
)

router = APIRouter()

@router.get("/", response_description="Tournaments retrieved")
async def get_tournaments():
    tournaments = await retrieve_tournaments()
    if tournaments:
        return ResponseModel(tournaments, "Tournaments data retrieved successfully")
    return ResponseModel(tournaments, "Empty list returned")