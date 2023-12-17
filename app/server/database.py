from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = "mongodb+srv://shourisingaraju:5wuLcbN9W3RXxUA@cluster0.5s0wiq8.mongodb.net/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.webapp

tournament_collection = database.get_collection("tournament")
booking_collection = database.get_collection("booking")
user_collection = database.get_collection("user")
location_collection = database.get_collection("location")
venue_collection = database.get_collection("venue")

#helpers

def tournament_helper(tournament) -> dict:
    return {
        "tournamentID": int(tournament["tournamentID"]),
        "tournamentName": str(tournament["tournamentName"]),
    }
def booking_helper(booking) -> dict:
    return {
        "_id": str(booking["_id"]),
        "bookingID": int(booking["bookingID"]),
        "userID": int(booking["userID"]),
        "bookingDate": str(booking["bookingDate"]),
        "venueID": int(booking["venueID"]),
        "venueName": str(booking["venueName"]),
        "courtID": int(booking["courtID"]),
        "courtName": str(booking["courtName"]),
        "slot": str(booking["slot"]),
        "paymentID": int(booking["paymentID"]),
        "amount": str(booking["amount"])
    }

def payment_helper(payment) -> dict:
    return{
        "bookingID": str(payment["bookingID"]),
        "bookingDate": str(payment["bookingDate"]),
        "amount": str(payment["amount"]),
        "firstName": str(payment["firstName"]),
        "lastName": str(payment["lastName"]),
    }
def user_helper(user) -> dict:
    return{
        "userID": int(user["userID"]),
        "firstName": str(user["firstName"]),
        "lastName": str(user["lastName"]),
        "mobile": str(user["mobile"]),
    }
# Retrieve all tournaments present in the database
async def retrieve_tournaments():
    tournaments = []
    async for tournament in tournament_collection.find():
        tournaments.append(tournament_helper(tournament))
    return tournaments

# Create booking in present database
async def add_booking(booking_data: dict) -> dict:
    booking = await booking_collection.insert_one(booking_data)
    new_booking = await booking_collection.find_one({"_id": booking.inserted_id})
    return booking_helper(new_booking)

# Retreive all bookings in present database
async def retrieve_bookings():
    bookings = []
    async for booking in booking_collection.find():
        bookings.append(booking_helper(booking))
    return bookings

# Retrieve a booking with a matching ID
async def retrieve_booking(bookingId: int) -> dict:
    booking = await booking_collection.find_one({"bookingID": int(bookingId)})
    if booking:
        return booking_helper(booking)

# Retreive all payments in present database
async def retreive_payments():
    payments = []
    async for payment in booking_collection.find():
        payments.append(payment_helper(payment))
    return payments

# Retreive all users in present database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

# Create user in present database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retreive slots for each venue
pipeline = [ 
    { 
        "$group" : {
            "_id": "$venueName",
            "amount" : { "$first": '$Amount' },
            "slots": { "$push": { "slot": "$slot", "isAvailable": "$isAvailable" } }
        }
    }
]

# Retreive slots data for each venue
async def retreive_slots():
    slots = []
    async for slot in location_collection.aggregate(pipeline):
        slots.append(slot)
    return slots

venue_pipeline = [
    {
        "$lookup" : {
            "from": "court",
            "localField": "courtID_one",
            "foreignField": "courtID",
            "as": "court1"
        }
    },
    { 
        "$lookup" : {
            "from": "court",
            "localField": "courtID_two",
            "foreignField": "courtID",
            "as": "court2"
        }
    }
]

# Retreive courts data for each venue
async def retreive_venues():
    venues = []
    async for venue in venue_collection.aggregate(venue_pipeline):
        venues.append(venue)
    return venues