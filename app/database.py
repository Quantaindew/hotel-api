#app/database.py
from pymongo import MongoClient
from bson import ObjectId
from .config import settings
from datetime import datetime


client = MongoClient(settings.mongodb_uri)
db = client[settings.database_name]

def create_hotel(hotel_data: dict) -> dict:
    """Create a new hotel and return its ID."""
    hotel_data["rooms"] = []  # Initialize with no rooms
    return db.hotels.insert_one(hotel_data).inserted_id

def add_room_to_hotel(hotel_id: str, room_data: dict) -> dict:
    """Add a new room to an existing hotel."""
    room_id = db.rooms.insert_one(room_data).inserted_id
    db.hotels.update_one({"_id": ObjectId(hotel_id)}, {"$push": {"rooms": room_id}})
    return room_id

# You can define more functions for updating and retrieving hotels and rooms as needed.
# Assuming this function is in database.py and is used to fetch all hotels
def get_all_hotels() -> list:
    hotels_cursor = db.hotels.find()
    hotels = []
    for hotel in hotels_cursor:
        # Convert each room's ObjectId to a string
        if 'rooms' in hotel:
            hotel['rooms'] = [str(room_id) for room_id in hotel['rooms']]
        # Convert the hotel's ObjectId to a string
        hotel['id'] = str(hotel['_id'])
        del hotel['_id']  # Remove the original '_id' field to avoid confusion
        hotels.append(hotel)
    return hotels

def get_all_rooms() -> list:
    """Retrieve all rooms across all hotels."""
    rooms = db.rooms.find()  # This fetches all rooms
    # Transform ObjectId to string since Pydantic models expect 'id' as a string
    return [{"id": str(room["_id"]), **room} for room in rooms]


def get_rooms_by_hotel(hotel_id: str) -> list:
    """Retrieve all rooms for a specific hotel."""
    hotel = db.hotels.find_one({"_id": ObjectId(hotel_id)})
    if not hotel or "rooms" not in hotel:
        return []
    
    # Since hotel["rooms"] already contains ObjectId instances, no need to transform them
    room_ids = hotel["rooms"]
    rooms = db.rooms.find({"_id": {"$in": room_ids}})
    return [{"id": str(room["_id"]), **room} for room in rooms]

# app/database.py (Add to existing functions)

def create_customer(customer_data: dict) -> dict:
    return db.customers.insert_one(customer_data).inserted_id

def create_booking(booking_data: dict) -> dict:
    return db.bookings.insert_one(booking_data).inserted_id

def get_available_rooms(start_date: datetime) -> list:
    # Convert start_date to datetime if it's not already
    if not isinstance(start_date, datetime):
        start_date = datetime.fromisoformat(start_date)

    # Find bookings that conflict with the given start_date
    conflicting_bookings = db.bookings.find({
        "end_date": {"$gte": start_date},
    })

    booked_room_ids = [booking["room_id"] for booking in conflicting_bookings]

    # Convert room_id strings to ObjectId instances for the query
    booked_room_object_ids = [ObjectId(room_id) for room_id in booked_room_ids]

    # Find rooms not in the list of booked_room_ids
    available_rooms = db.rooms.find({
        "_id": {"$nin": booked_room_object_ids}
    })

    # Return the rooms, converting ObjectId to string in the process
    return [{"id": str(room["_id"]), **room} for room in available_rooms]
