from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retreive_dashboard_data
)
from app.server.models.dashboard import (
    ErrorResponseModel,
    ResponseModel,
    DashboardSchema
)

router = APIRouter()

@router.get("/", response_description="Dashboard data retrieved")
async def get_dashboard_data():
    dashboard_data = await retreive_dashboard_data()
    if dashboard_data:
        return dashboard_data
    return ResponseModel([], "Empty list returned")