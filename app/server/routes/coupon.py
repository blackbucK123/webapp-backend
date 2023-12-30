from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
   retreive_coupons
)
from app.server.models.coupon import (
    ErrorResponseModel,
    ResponseModel,
    CouponSchema
)

router = APIRouter()

@router.get("/", response_description="Coupons retrieved")
async def get_coupons():
    try:
        coupons = await retreive_coupons()
        if coupons:
            return coupons
        else:
            return ResponseModel([], "No venues coupons")
    except Exception as e:
        return ErrorResponseModel(str(e), 400, "An error occurred while retrieving coupons")