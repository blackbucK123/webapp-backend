from typing import List
from pydantic import BaseModel, Field

class BookingData(BaseModel):
    bookingID: int
    bookingDate: str
    tournamentName: str

class CouponSchema(BaseModel):
    couponID: int = Field(...)
    userID: int = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    couponDate: str = Field(...)
    isRedeemed: bool = Field(...)
    bookings: List[int] = []
    bookingData: List[BookingData] = []

class CouponCreateSchema(BaseModel):
    couponID: int = Field(...)
    userID: int = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    couponDate: str = Field(...)
    isRedeemed: bool = Field(...)
   

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}