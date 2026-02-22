"""Hotel module for the Reservation System."""

import json
import os

HOTELS_FILE = "hotels.json"


class Hotel:
    """Represents a hotel with rooms and reservations."""

    def __init__(self, hotel_id, name, location, total_rooms):
        """Initialize a Hotel instance."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms
        self.reservations = []

    def to_dict(self):
        """Convert Hotel to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
            "reservations": self.reservations,
        }

    @staticmethod
    def from_dict(data):
        """Create a Hotel from a dictionary."""
        hotel = Hotel(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["total_rooms"],
        )
        hotel.available_rooms = data.get("available_rooms", hotel.total_rooms)
        hotel.reservations = data.get("reservations", [])
        return hotel

    @staticmethod
    def _load_hotels():
        """Load all hotels from file."""
        if not os.path.exists(HOTELS_FILE):
            return {}
        try:
            with open(HOTELS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            hotels = {}
            for k, v in data.items():
                try:
                    hotels[k] = Hotel.from_dict(v)
                except (KeyError, TypeError) as e:
                    print(f"Error loading hotel record '{k}': {e}")
            return hotels
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading hotels file: {e}")
            return {}

    @staticmethod
    def _save_hotels(hotels):
        """Save all hotels to file."""
        try:
            with open(HOTELS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {k: v.to_dict() for k, v in hotels.items()}, f, indent=4
                )
        except OSError as e:
            print(f"Error saving hotels file: {e}")

    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms):
        """Create and persist a new hotel."""
        hotels = Hotel._load_hotels()
        if hotel_id in hotels:
            print(f"Hotel '{hotel_id}' already exists.")
            return None
        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel
        Hotel._save_hotels(hotels)
        print(f"Hotel '{name}' created successfully.")
        return hotel

    @staticmethod
    def delete_hotel(hotel_id):
        """Delete a hotel by ID."""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Hotel '{hotel_id}' not found.")
            return False
        del hotels[hotel_id]
        Hotel._save_hotels(hotels)
        print(f"Hotel '{hotel_id}' deleted successfully.")
        return True

    @staticmethod
    def display_hotel(hotel_id):
        """Display hotel information."""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Hotel '{hotel_id}' not found.")
            return None
        hotel = hotels[hotel_id]
        print(f"Hotel ID   : {hotel.hotel_id}")
        print(f"Name       : {hotel.name}")
        print(f"Location   : {hotel.location}")
        print(f"Total Rooms: {hotel.total_rooms}")
        print(f"Available  : {hotel.available_rooms}")
        print(f"Reservations: {hotel.reservations}")
        return hotel

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None, total_rooms=None):
        """Modify hotel information."""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Hotel '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        if name:
            hotel.name = name
        if location:
            hotel.location = location
        if total_rooms is not None:
            diff = total_rooms - hotel.total_rooms
            hotel.total_rooms = total_rooms
            hotel.available_rooms = max(0, hotel.available_rooms + diff)
        Hotel._save_hotels(hotels)
        print(f"Hotel '{hotel_id}' modified successfully.")
        return True

    @staticmethod
    def reserve_room(hotel_id, reservation_id):
        """Reserve a room in the hotel."""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Hotel '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        if hotel.available_rooms <= 0:
            print(f"No available rooms in hotel '{hotel_id}'.")
            return False
        hotel.available_rooms -= 1
        hotel.reservations.append(reservation_id)
        Hotel._save_hotels(hotels)
        print(f"Room reserved in hotel '{hotel_id}' for reservation '{reservation_id}'.")
        return True

    @staticmethod
    def cancel_room(hotel_id, reservation_id):
        """Cancel a room reservation in the hotel."""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Hotel '{hotel_id}' not found.")
            return False
        hotel = hotels[hotel_id]
        if reservation_id not in hotel.reservations:
            print(f"Reservation '{reservation_id}' not found in hotel '{hotel_id}'.")
            return False
        hotel.reservations.remove(reservation_id)
        hotel.available_rooms = min(hotel.total_rooms, hotel.available_rooms + 1)
        Hotel._save_hotels(hotels)
        print(f"Reservation '{reservation_id}' cancelled in hotel '{hotel_id}'.")
        return True
