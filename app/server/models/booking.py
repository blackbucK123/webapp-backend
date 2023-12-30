from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BookingSchema(BaseModel):
    # id: Optional[PyObjectId] = Field(alias='_id') # was using this for testing
    bookingID: int = Field(...)
    userID: int = Field(...)
    bookingDate: str = Field(...)
    venueID: int = Field(...)
    venueName: str = Field(...)
    courtID: int = Field(...)
    courtName: str = Field(...)
    slot: str = Field(...)
    paymentID: str = Field(...)
    amount: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    mobile: str = Field(...)
    tournamentName: str = Field(...)
    isRedeemed: bool = Field(...)
    

    class Config:
        schema_extra = {
            "example": {
                "bookingID": 10001,
                "venueName": "Gachibowli Stadium",
                "courtName": "Court 1",
                "firstName": "Shouri",
                "mobile": "6281353466",
                "tournamentName": "1v1",
                "isRedeemed": True
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