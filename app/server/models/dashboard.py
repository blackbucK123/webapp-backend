from typing import Optional
from pydantic import BaseModel, Field


class DashboardSchema(BaseModel):
    booking_count: int 
    user_count: int
    coupon_count: int

    class Config:
        schema_extra = {
            "example": {
                "booking_count": 1,
                "user_count": 1,
                "coupon_count": 1,
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}