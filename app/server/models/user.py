from typing import Optional
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    userID: int = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    mobile: str = Field(...)
   

    class Config:
        schema_extra = {
            "example": {
                "userID": 1,
                "firstName": "Shouri",
                "lastName": "Singaraju",
                "mobile": "6281353466"
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