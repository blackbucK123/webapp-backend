from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
   retrieve_users,
   add_user,
   retrieve_user
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema
)

router = APIRouter()

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/{mobile}", response_description="User data retrieved")
async def get_user_data(mobile):
    user = await retrieve_user(mobile)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user = await add_user(user)
    return ResponseModel(user, "User added successfully.")