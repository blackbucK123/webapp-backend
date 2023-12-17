from typing import Optional
from pydantic import BaseModel, Field


class TournamentSchema(BaseModel):
    tournamentID: int = Field(...)
    tournamentName: str = Field(...)
   
    class Config:
        schema_extra = {
            "example": {
                "tournamentID": 1,
                "tournamentName": "1v1"
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