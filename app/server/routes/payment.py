from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
   retreive_payments
)
from app.server.models.payment import (
    ErrorResponseModel,
    ResponseModel,
    PaymentSchema
)

router = APIRouter()

@router.get("/", response_description="Payments retrieved")
async def get_payments():
    payments = await retreive_payments()
    if payments:
        return ResponseModel(payments, "Payments data retrieved successfully")
    return ResponseModel(payments, "Empty list returned")
