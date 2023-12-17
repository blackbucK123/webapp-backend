from typing import List
from pydantic import BaseModel, Field


class PaymentSchema(BaseModel):
    bookingID: int = Field(...)
    bookingDate: str = Field(...)
    amount: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    class Config:
            schema_extra = {
                "example": {
                    "bookingID": 10001,
                    "bookingDate": "11-12-2023",
                    "amount": "₹ 350.00",
                    "firstName": "Shouri",
                    "lastName": "Singaraju",
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