# app/routes.py
from fastapi import APIRouter, HTTPException, Body
from .models import HotelCreate, RoomCreate, Hotel, Room, Customer, CustomerCreate, Booking, BookingCreate
from .database import create_hotel,create_customer, create_booking, add_room_to_hotel, get_all_hotels, get_all_rooms, get_rooms_by_hotel, get_available_rooms
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/add-hotel/", response_model=Hotel)
def create_hotel_route(hotel: HotelCreate):
    hotel_id = create_hotel(hotel.dict())
    return {**hotel.dict(), "id": str(hotel_id), "rooms": []}


@router.post("/hotels/{hotel_id}/add-room/", response_model=Room)
def add_room_route(hotel_id: str, room: RoomCreate):
    # Ensure the hotel_id is stored with the room
    room_data = room.dict()
    room_data["hotel_id"] = hotel_id  # Add hotel_id to the room document
    room_id = add_room_to_hotel(hotel_id, room_data)
    return {**room_data, "id": str(room_id)}

@router.get("/get-all-hotels/", response_model=List[Hotel])
def read_all_hotels():
    return get_all_hotels()

@router.get("/get-all-rooms/", response_model=List[Room])
def read_all_rooms():
    rooms = get_all_rooms()
    return rooms

@router.get("/hotels/{hotel_id}/get-rooms/", response_model=List[Room])
def read_rooms_by_hotel(hotel_id: str):
    rooms = get_rooms_by_hotel(hotel_id)
    if not rooms:
        raise HTTPException(status_code=404, detail="Hotel not found or no rooms available")
    return rooms

# app/routes.py (Add to existing routes)

@router.post("/create-customer/", response_model=Customer)
def create_customer_route(customer: CustomerCreate):
    customer_id = create_customer(customer.dict())
    return {**customer.dict(), "id": str(customer_id)}

@router.post("/create-bookings/", response_model=Booking)
def create_booking_route(booking: BookingCreate):
    booking_id = create_booking(booking.dict())
    return {**booking.dict(), "id": str(booking_id)}

@router.get("/get-available-rooms/", response_model=List[Room])
def get_available_rooms_route(start_date: datetime):
    rooms = get_available_rooms(start_date)
    return rooms
