from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.database import (
   retreive_coupons,
   add_coupon,
   redeem_coupon,
   retrieve_user_coupons
)
from app.server.models.coupon import (
    ErrorResponseModel,
    ResponseModel,
    CouponSchema,
    CouponCreateSchema
)

router = APIRouter()

@router.get("/", response_model=List[CouponSchema])
async def get_coupons():
    try:
        coupons = await retreive_coupons()
        if coupons:
            return coupons
        else:
            return ResponseModel([], "No new coupons")
    except Exception as e:
        return ErrorResponseModel(str(e), 400, "An error occurred while retrieving coupons")
    
@router.post("/", response_description="Coupon added into the database")
async def add_coupon_data(coupon: CouponCreateSchema = Body(...)):
    coupon = jsonable_encoder(coupon)
    new_coupon, message = await add_coupon(coupon)
    return ResponseModel(new_coupon, message)

@router.put("/{couponID}", response_description="Coupon redeemed successfully")
async def redeem_coupon_code(couponID: int):
    # Redeem the coupon
    updated_coupon = await redeem_coupon(couponID)
    
    # Check if the coupon was successfully redeemed
    if updated_coupon:
        return updated_coupon
    
    # If no coupon was found with the given ID, return an error response
    return ErrorResponseModel("Coupon not found or already redeemed", 404, "Coupon not found or already redeemed")


@router.get("/{userID}", response_model=List[CouponSchema])
async def get_coupon_data(userID):
    try:
        coupons = await retrieve_user_coupons(userID)
        if coupons:
            return coupons  # Return the list of coupons directly
        else:
            return []  # Return an empty list if no coupons are found
    except Exception as e:
        return ErrorResponseModel(str(e), 400, "An error occurred while retrieving coupons")