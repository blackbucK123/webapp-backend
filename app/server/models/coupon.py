from typing import List
from pydantic import BaseModel, Field

class BookingData(BaseModel):
    bookingID: int
    bookingDate: str
    tournamentName: str

class CouponSchema(BaseModel):
    couponID: int = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    couponDate: str = Field(...)
    bookings: List[int] = []
    bookingData: List[BookingData] = []
   
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             {
    #                 "couponID": 1,
    #                 "firstName": "Shouri",
    #                 "lastName": "Singaraju",
    #                 "couponDate": "18-12-2023",
    #                 "bookings": [
    #                     10001,
    #                     10002,
    #                     10003,
    #                     10004,
    #                     10005
    #                 ],
    #                 "bookingData": [
    #                             {
    #                             "bookingID": 10001,
    #                             "bookingDate": "11-12-2023",
    #                             "tournamentName": "1v1"
    #                             },
    #                             {
    #                             "bookingID": 10002,
    #                             "bookingDate": "12-12-2023",
    #                             "tournamentName": "3 Point Contest"
    #                             },
    #                             {
    #                             "bookingID": 10003,
    #                             "bookingDate": "13-12-2023",
    #                             "tournamentName": "Dunk Contest"
    #                             },
    #                             {
    #                             "bookingID": 10004,
    #                             "bookingDate": "14-12-2023",
    #                             "tournamentName": "1v1"
    #                             },
    #                             {
    #                             "bookingID": 10005,
    #                             "bookingDate": "15-12-2023",
    #                             "tournamentName": "5v5"
    #                             }
    #                     ]
    #             }
    #         }
    #     }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}