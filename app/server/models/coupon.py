from typing import List
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

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

class BookingData(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id') 
    bookingID: int
    bookingDate: str
    tournamentName: str

class CouponSchema(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id') 
    bookingData: List[BookingData] = []
    bookings: List[int] = []
    couponDate: str = Field(...)
    couponID: int = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    isRedeemed: bool = Field(...)
    userID: int = Field(...)
    
    

    class Config:
        schema_extra = {
            "example": {
            "couponID": 1,
            "userID": 1,
            "firstName": "Shouri",
            "lastName": "Singaraju",
            "couponDate": "18-12-2023",
            "isRedeemed": True,
            "bookings": [
                10001,
                10002,
                10003,
                10004,
                10005
            ],
            "bookingData": [
                {
                "bookingID": 10002,
                "bookingDate": "12-12-2023",
                "tournamentName": "3 Point Contest"
                },
                {
                "bookingID": 10005,
                "bookingDate": "15-12-2023",
                "tournamentName": "5v5"
                },
                {
                "bookingID": 10004,
                "bookingDate": "14-12-2023",
                "tournamentName": "1v1"
                },
                {
                "bookingID": 10001,
                "bookingDate": "11-12-2023",
                "tournamentName": "1v1"
                },
                {
                "bookingID": 10003,
                "bookingDate": "13-12-2023",
                "tournamentName": "Dunk Contest"
                }
            ]
            }
        }

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