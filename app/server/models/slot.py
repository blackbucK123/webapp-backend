from typing import Optional, List
from pydantic import BaseModel, Field


class SlotSchema(BaseModel):
    _id: str = None
    amount: int = None
    slots: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "_id": "Gachibowli Stadium",
                "slots": [
                    "08:00 AM",
                    "09:00 AM",
                    "10:00 AM",
                    "11:00 AM",
                    "12:00 PM",
                    "01:00 PM"
                ]
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