from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
   retreive_coupons,
   add_coupon,
   redeem_coupon
)
from app.server.models.coupon import (
    ErrorResponseModel,
    ResponseModel,
    CouponSchema,
    CouponCreateSchema
)

router = APIRouter()

@router.get("/", response_model=CouponSchema)
async def get_coupons():
    try:
        coupons = await retreive_coupons()
        if coupons:
            return coupons
        else:
            return ResponseModel([], "No venues coupons")
    except Exception as e:
        return ErrorResponseModel(str(e), 400, "An error occurred while retrieving coupons")
    
@router.post("/", response_description="Coupon added into the database")
async def add_coupon_data(coupon: CouponCreateSchema = Body(...)):
    coupon = jsonable_encoder(coupon)
    new_coupon, message = await add_coupon(coupon)
    return ResponseModel(new_coupon, message)

@router.put("/{couponID}", response_description="Coupon redeemed successfully")
async def redeem_coupon_code(couponID: int):
    coupon = await redeem_coupon(couponID)
    if coupon:
        return ResponseModel(coupon, "Coupon redeemed successfully")
    return ErrorResponseModel("An error occurred.", 404, "Coupon redeemed already")