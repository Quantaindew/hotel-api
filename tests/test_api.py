# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import path based on your project structure

client = TestClient(app)

def test_create_hotel():
    response = client.post(
        "/add-hotel/",
        json={"name": "Test Hotel", "description": "A description", "location": "Test Location"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hotel"
    assert "id" in data
    return data["id"]

def test_add_room_to_hotel():
    hotel_id = test_create_hotel()  # Reusing the test to create a hotel for adding a room
    response = client.post(
        f"/hotels/{hotel_id}/add-room/",
        json={"description": "A room description", "price_per_night": 100, "features": {"breakfast_included": True, "has_air_conditioning": True, "has_sea_view": False}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "A room description"
    assert "id" in data

def test_get_all_rooms():
    response = client.get("/get-all-rooms/")
    assert response.status_code == 200
    rooms = response.json()
    assert isinstance(rooms, list)  # Adjust according to your actual data model

def test_get_rooms_by_hotel():
    hotel_id = test_create_hotel()  # Ensuring there's at least one hotel to test with
    response = client.get(f"/hotels/{hotel_id}/get-rooms/")
    assert response.status_code == 200
    rooms = response.json()
    assert isinstance(rooms, list)  # Adjust according to your actual data model
