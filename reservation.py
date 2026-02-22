"""Reservation module for the Reservation System."""

import json
import os

from hotel import Hotel
from customer import Customer

RESERVATIONS_FILE = "reservations.json"


class Reservation:
    """Represents a reservation linking a customer to a hotel."""

    def __init__(self, reservation_id, customer_id, hotel_id, check_in, check_out):
        """Initialize a Reservation instance."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out

    def to_dict(self):
        """Convert Reservation to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }

    @staticmethod
    def from_dict(data):
        """Create a Reservation from a dictionary."""
        return Reservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["check_in"],
            data["check_out"],
        )

    @staticmethod
    def _load_reservations():
        """Load all reservations from file."""
        if not os.path.exists(RESERVATIONS_FILE):
            return {}
        try:
            with open(RESERVATIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            reservations = {}
            for k, v in data.items():
                try:
                    reservations[k] = Reservation.from_dict(v)
                except (KeyError, TypeError) as e:
                    print(f"Error loading reservation record '{k}': {e}")
            return reservations
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading reservations file: {e}")
            return {}

    @staticmethod
    def _save_reservations(reservations):
        """Save all reservations to file."""
        try:
            with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {k: v.to_dict() for k, v in reservations.items()},
                    f,
                    indent=4,
                )
        except OSError as e:
            print(f"Error saving reservations file: {e}")

    @staticmethod
    def create_reservation(reservation_id, customer_id, hotel_id, check_in, check_out):
        """Create a new reservation."""
        reservations = Reservation._load_reservations()
        if reservation_id in reservations:
            print(f"Reservation '{reservation_id}' already exists.")
            return None

        # Validate customer and hotel exist
        customers = Customer._load_customers()
        if customer_id not in customers:
            print(f"Customer '{customer_id}' not found. Cannot create reservation.")
            return None

        # Reserve room in hotel (validates hotel exists and has availability)
        success = Hotel.reserve_room(hotel_id, reservation_id)
        if not success:
            return None

        reservation = Reservation(
            reservation_id, customer_id, hotel_id, check_in, check_out
        )
        reservations[reservation_id] = reservation
        Reservation._save_reservations(reservations)
        print(f"Reservation '{reservation_id}' created successfully.")
        return reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancel an existing reservation."""
        reservations = Reservation._load_reservations()
        if reservation_id not in reservations:
            print(f"Reservation '{reservation_id}' not found.")
            return False

        reservation = reservations[reservation_id]
        Hotel.cancel_room(reservation.hotel_id, reservation_id)
        del reservations[reservation_id]
        Reservation._save_reservations(reservations)
        print(f"Reservation '{reservation_id}' cancelled successfully.")
        return True

    @staticmethod
    def display_reservation(reservation_id):
        """Display reservation information."""
        reservations = Reservation._load_reservations()
        if reservation_id not in reservations:
            print(f"Reservation '{reservation_id}' not found.")
            return None
        res = reservations[reservation_id]
        print(f"Reservation ID: {res.reservation_id}")
        print(f"Customer ID   : {res.customer_id}")
        print(f"Hotel ID      : {res.hotel_id}")
        print(f"Check-in      : {res.check_in}")
        print(f"Check-out     : {res.check_out}")
        return res
