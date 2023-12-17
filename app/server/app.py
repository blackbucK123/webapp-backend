from fastapi import FastAPI

from app.server.routes.tournament import router as TournamentRouter
from app.server.routes.booking import router as BookingRouter
from app.server.routes.payment import router as PaymentRouter
from app.server.routes.user import router as UserRouter
from app.server.routes.slot import router as SlotRouter
from app.server.routes.venue import router as VenueRouter
from app.server.routes.otp import router as OTPRouter

app = FastAPI()

app.include_router(TournamentRouter, tags=["Tournament"], prefix="/tournaments")
app.include_router(BookingRouter, tags=["Booking"], prefix="/bookings")
app.include_router(PaymentRouter, tags=['Payment'], prefix="/payments")
app.include_router(UserRouter, tags=['User'], prefix="/users")
app.include_router(SlotRouter, tags=['Slot'], prefix="/slots")
app.include_router(VenueRouter, tags=['Venue'], prefix="/venues")
app.include_router(OTPRouter, tags=['OTP'], prefix="/otp")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

