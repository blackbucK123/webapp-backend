from bson.objectid import ObjectId
import motor.motor_asyncio
from pprint import pprint
from bson import ObjectId

MONGO_DETAILS = "mongodb+srv://shourisingaraju:5wuLcbN9W3RXxUA@cluster0.5s0wiq8.mongodb.net/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.webapp

tournament_collection = database.get_collection("tournament")
booking_collection = database.get_collection("booking")
user_collection = database.get_collection("user")
location_collection = database.get_collection("location")
venue_collection = database.get_collection("venue")
coupon_collection = database.get_collection("coupons")
payment_collection = database.get_collection("payment")

#helpers

def tournament_helper(tournament) -> dict:
    return {
        "tournamentID": int(tournament["tournamentID"]),
        "tournamentName": str(tournament["tournamentName"]),
    }

def booking_helper(booking) -> dict:
    return {
        "bookingID": int(booking["bookingID"]),
        "userID": int(booking["userID"]),
        "bookingDate": str(booking["bookingDate"]),
        "venueID": int(booking["venueID"]),
        "venueName": str(booking["venueName"]),
        "courtID": int(booking["courtID"]),
        "courtName": str(booking["courtName"]),
        "slot": str(booking["slot"]),
        "paymentID": int(booking["paymentID"]),
        "amount": str(booking["amount"]),
        "firstName": str(booking["firstName"]),
        "lastName": str(booking['lastName']),
        "mobile": str(booking["mobile"]),
        "tournamentName": str(booking["tournamentName"]),
        "isRedeemed": bool(booking['isRedeemed'])
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
def coupon_helper(coupon) -> dict:
    return{
        "couponID": int(coupon['couponID']),
        "userID": int(coupon['userID']),
        "firstName": str(coupon['firstName']),
        "lastName": str(coupon['lastName']),
        "couponDate": str(coupon['couponDate']),
        "isRedeemed": bool(coupon['isRedeemed']),
        "bookings": coupon['bookings']
    }
# Retrieve all tournaments present in the database
async def retrieve_tournaments():
    tournaments = []
    async for tournament in tournament_collection.find():
        tournaments.append(tournament_helper(tournament))
    return tournaments

# Create booking in present database
async def add_booking(booking_data: dict) -> dict:
    max_payment_agregate = [{
        "$group" : {
            "_id": "null",
            "max_paymentID" : { "$max": "$paymentID"}
        }
    }]
    max_booking_agregate = [{
        "$group" : {
            "_id": "null",
            "max_bookingID" : { "$max": "$bookingID"}
        }
    }]
    async for payment in payment_collection.aggregate(max_payment_agregate):
        max_payment_id = int(payment['max_paymentID'])
       
    async for booking in booking_collection.aggregate(max_booking_agregate):
        max_booking_id = int(booking['max_bookingID'])

    payment_obj = {
        "paymentID": max_payment_id + 1,
        "bookingID": max_booking_id + 1,
        "userID": booking_data['userID'],
        "amount": booking_data['amount'],
        "paymentDate": booking_data['bookingDate']
    }

    payment = await payment_collection.insert_one(payment_obj)
    new_payment = await payment_collection.find_one({"_id": payment.inserted_id})

    if new_payment:
        booking_data['bookingID'] = max_booking_id + 1
        booking_data['paymentID'] = max_payment_id + 1
        booking_data['isRedeemed'] = False
        booking = await booking_collection.insert_one(booking_data)
        new_booking = await booking_collection.find_one({"_id": booking.inserted_id})
        return booking_helper(new_booking), 'Booking confirmed!'
    else:
        return [], "Payment confirmation pending!"

# Retreive all bookings in present database
async def retrieve_bookings():
    bookings = []
    async for booking in booking_collection.find():
        bookings.append(booking_helper(booking))
    return bookings, "Booking confirmed!"

# Retrieve a booking with a matching ID
async def retrieve_booking(userID: int):
    bookings = []
    async for booking in booking_collection.find({"userID": int(userID)}):
        bookings.append(booking_helper(booking))
    return bookings

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

# Retrieve a booking with a matching ID
async def retrieve_user(mobile: str) -> dict:
    user = await user_collection.find_one({"mobile": str(mobile)})
    if user:
        return user_helper(user)

# Create user in present database
async def add_user(user_data: dict) -> dict:
    max_user_agregate = [{
        "$group" : {
            "_id": "null",
            "max_userID" : { "$max": "$userID"}
        }
    }]
    user = await user_collection.find_one({"mobile": str(user_data['mobile'])})
    
    if user is not None:
        return {}
    async for user in user_collection.aggregate(max_user_agregate):
        max_user_id = int(user['max_userID'])
    
    user_data['userID'] = max_user_id + 1
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

booking_count = [
     { 
        "$group" : {
            "_id": "null",
            "booking_count": { "$count": { } }
        }
    }
]
coupon_count = [
     { 
        "$group" : {
            "_id": "null",
            "coupon_count": { "$count": { } }
        }
    }
]
user_count = [
     { 
        "$group" : {
            "_id": "null",
            "user_count": { "$count": { } }
        }
    }
]
# Retreive dashboard data 
async def retreive_dashboard_data():
    booking_num = 0
    coupon_num = 0
    user_num = 0
    async for bookings in booking_collection.aggregate(booking_count):
        booking_num = int(bookings["booking_count"])
    async for coupons in coupon_collection.aggregate(coupon_count):
        coupon_num = int(coupons["coupon_count"])
    async for users in user_collection.aggregate(user_count):
        user_num = int(users["user_count"])
    resp = {
        "booking_count": booking_num,
        "user_count": user_num,
        "coupon_count": coupon_num
    }
    return resp

coupon_pipeline = [
    {
        "$lookup": {
            "from": "booking",
            "let": { "bookingIds": "$bookings" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$in": ["$bookingID", "$$bookingIds"]
                        }
                    }
                },
                {
                    "$project": {
                        "bookingID": 1,
                        "bookingDate": 1, 
                        "tournamentName": 1  
                    }
                }
            ],
            "as": "bookingData"
        }
    }
]
"""
max_user_agregate = [{
        "$group" : {
            "_id": "null",
            "max_userID" : { "$max": "$userID"}
        }
    }]
    async for user in user_collection.aggregate(max_user_agregate):
        max_user_id = int(user['max_userID'])
    
    user_data['userID'] = max_user_id + 1
"""
# Retreive courts data for each venue
async def retreive_coupons():
    coupons = []
    # coupon = await coupon_collection.aggregate(coupon_pipeline)
    async for coupon in coupon_collection.aggregate(coupon_pipeline):
        coupons.append(coupon)
    return coupons


# Retrieve a booking with a matching ID
async def retrieve_user_coupons(userID: int):
    coupons = []
    pipeline = [
        {
            "$match": {
                "userID":int(userID)
            }
        },
        {
            "$lookup": {
                "from": "booking",
                "let": { "bookingIds": "$bookings" },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$in": ["$bookingID", "$$bookingIds"]
                            }
                        }
                    },
                    {
                        "$project": {
                            "bookingID": 1,
                            "bookingDate": 1, 
                            "tournamentName": 1  
                        }
                    }
                ],
                "as": "bookingData"
            }
        }
    ]
    async for coupon in coupon_collection.aggregate(pipeline):
        coupons.append(coupon)
    if len(coupons) == 0:
        return []
    elif len(coupons) < 2:
        return [coupon]
    else:
        pprint(coupons)
        return coupons


# Create new coupon if 5 bookings made since last time
async def add_coupon(coupon_data: dict) -> dict:
    bookings = []
    query = {"$and": [{"userID": coupon_data['userID']}, {"isRedeemed": False}]}

    max_coupon_agregate = [{
        "$group" : {
            "_id": "null",
            "max_couponID" : { "$max": "$couponID"}
        }
    }]

    async for coupon in coupon_collection.aggregate(max_coupon_agregate):
        max_coupon_id = int(coupon['max_couponID'])

    async for booking in booking_collection.find(query):
        bookings.append(booking["bookingID"])


    if len(bookings) == 5:
        coupon_data['bookings'] = bookings
        coupon_data['couponID'] = max_coupon_id + 1
        coupon = await coupon_collection.insert_one(coupon_data)
        new_coupon = await coupon_collection.find_one({"_id": coupon.inserted_id})
        for booking in bookings:
             await booking_collection.update_one({"bookingID": booking}, { "$set": { "isRedeemed": True }})
        return coupon_helper(new_coupon), "Coupon added!!!"
    elif len(bookings) < 5:
        return [], "No coupon for now!!!"
    
# Update coupon status if redeemed
async def redeem_coupon(couponID: int) -> dict:
    # Perform the update operation
    update_result = await coupon_collection.update_one(
        {"couponID": int(couponID)},
        {"$set": {"isRedeemed": True}}  # Set the isRedeemed field to True
    )
    
    # Check if the update operation was successful
    if update_result.modified_count > 0:
        # If the document was updated, query and return the updated document
        updated_coupon = await coupon_collection.find_one({"couponID": int(couponID)})
        return coupon_helper(updated_coupon)
    
    # If the update operation failed (no documents matched the filter), return None
    return None