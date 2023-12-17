from typing import Optional

from pydantic import BaseModel, Field


class BookingSchema(BaseModel):
    _id: str = Field(...)
    bookingID: int = Field(...)
    userID: int = Field(...)
    bookingDate: str = Field(...)
    venueID: int = Field(...)
    venueName: str = Field(...)
    courtID: int = Field(...)
    courtName: str = Field(...)
    slot: str = Field(...)
    paymentID: int = Field(...)
    amount: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "bookingID": 10001,
                "userID": 1,
                "bookingDate": "11-12-2023",
                "venueID": 1,
                "venueName": "Gachibowli Stadium",
                "courtID": 11,
                "courtName": "Court 1",
                "slot": "12:00 PM",
                "paymentID": 1,
                "amount": "₹ 350.00"
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