from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RoomFeatures(BaseModel):
    breakfast_included: bool
    has_air_conditioning: bool
    has_sea_view: bool

class RoomBase(BaseModel):
    description: str
    price_per_night: float
    features: RoomFeatures

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: str

    class Config:
        # Updated for Pydantic v2.x
        populate_by_name = True  
        json_schema_extra = {
            "example": {
                "description": "A room with a beautiful sea view, inclusive of breakfast and air conditioning.",
                "price_per_night": 120.00,
                "features": {
                    "breakfast_included": True,
                    "has_air_conditioning": True,
                    "has_sea_view": True
                }
            }
        }

class HotelBase(BaseModel):
    name: str
    description: str
    location: str

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: str
    rooms: List[str] = []

    class Config:
        # Updated for Pydantic v2.x
        populate_by_name = True  
        json_schema_extra = {
            "example": {
                "name": "Ocean View Retreat",
                "description": "A hotel with a stunning view of the ocean, providing a perfect escape from the city.",
                "location": "123 Beach Ave, Ocean City",
                "rooms": []  # Will be filled with room IDs
            }
        }

# Model for updating hotel information
class HotelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    class Config:
        # Updated for Pydantic v2.x
        json_schema_extra = {
            "example": {
                "name": "Ocean View Retreat",
                "description": "An updated description of the hotel.",
                "location": "An updated address if needed."
            }
        }

# Model for updating room information
class RoomUpdate(BaseModel):
    description: Optional[str] = None
    price_per_night: Optional[float] = None
    features: Optional[RoomFeatures] = None

    class Config:
        # Updated for Pydantic v2.x
        json_schema_extra = {
            "example": {
                "description": "A newly refurbished room with an amazing mountain view.",
                "price_per_night": 150.00,
                "features": {
                    "breakfast_included": True,
                    "has_air_conditioning": True,
                    "has_sea_view": False
                }
            }
        }


# app/models.py (Add to existing models)


class CustomerBase(BaseModel):
    name: str
    email: str
    number: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: str

class BookingBase(BaseModel):
    customer_id: str
    room_id: str
    start_date: datetime
    end_date: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: str
