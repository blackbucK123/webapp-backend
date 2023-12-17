from typing import Optional, List
from pydantic import BaseModel, Field

class Court(BaseModel):
    courtID: int = Field(...)
    courtName: str = Field(...)
    scheduleID_one: int = Field(...)
    scheduleID_two: int = Field(...)
    scheduleID_three: int = Field(...)
 

class VenueSchema(BaseModel):
    court1: List[Court] = []
    court2: List[Court] = []
    venueID: int = Field(...)
    venueName: str = Field(...)
    courtID_one: int = Field(...)
    courtID_two: int = Field(...)
  

    class Config:
        schema_extra = {
            "example": {
                "court1": [
                    {
                    "courtID": 11,
                    "courtName": "Court 1",
                    "scheduleID_one": 111,
                    "scheduleID_two": 222,
                    "scheduleID_three": 333
                    }
                ],
                "court2": [
                    {
                    "courtID": 12,
                    "courtName": "Court 2",
                    "scheduleID_one": 111,
                    "scheduleID_two": 222,
                    "scheduleID_three": 333
                    }
                ],
                "venueID": 1,
                "venueName": "Gachibowli Stadium",
                "courtID_one": 11,
                "courtID_two": 12,
            }
        }

def ResponseModel(data, message):
    return {
        "data": data if isinstance(data, list) else [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}