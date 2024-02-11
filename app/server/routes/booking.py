from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_booking,
    retrieve_bookings,
    retrieve_booking
)
from app.server.models.booking import (
    ErrorResponseModel,
    ResponseModel,
    BookingSchema
)

router = APIRouter()

@router.get("/", response_description="Bookings retrieved")
async def get_bookings():
    bookings = await retrieve_bookings()
    if bookings:
        return ResponseModel(bookings, "Bookingss data retrieved successfully")
    return ResponseModel(bookings, "Empty list returned")

@router.get("/{userID}", response_description="Booking data retrieved")
async def get_booking_data(userID):
    booking = await retrieve_booking(userID)
    if booking:
        return ResponseModel(booking, "Booking data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Booking doesn't exist.")

@router.post("/", response_description="Booking data added into the database")
async def add_booking_data(booking: BookingSchema = Body(...)):
    booking = jsonable_encoder(booking)
    new_booking, message = await add_booking(booking)
    return ResponseModel(new_booking, message)