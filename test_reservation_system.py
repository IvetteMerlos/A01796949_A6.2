"""Unit tests for Hotel Reservation System."""

import json
import os
import unittest
from unittest.mock import patch

from hotel import Hotel, HOTELS_FILE
from customer import Customer, CUSTOMERS_FILE
from reservation import Reservation, RESERVATIONS_FILE


def remove_test_files():
    """Remove data files used during tests."""
    for f in [HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE]:
        if os.path.exists(f):
            os.remove(f)


class TestHotel(unittest.TestCase):
    """Test cases for the Hotel class."""

    def setUp(self):
        remove_test_files()

    def tearDown(self):
        remove_test_files()

    # --- create_hotel ---
    def test_create_hotel_success(self):
        hotel = Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Grand Inn")
        self.assertEqual(hotel.available_rooms, 50)

    def test_create_hotel_duplicate(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        result = Hotel.create_hotel("H1", "Other", "LA", 10)
        self.assertIsNone(result)

    def test_create_hotel_persists(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        self.assertTrue(os.path.exists(HOTELS_FILE))

    # --- delete_hotel ---
    def test_delete_hotel_success(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        result = Hotel.delete_hotel("H1")
        self.assertTrue(result)

    def test_delete_hotel_not_found(self):
        result = Hotel.delete_hotel("NONEXISTENT")
        self.assertFalse(result)

    # --- display_hotel ---
    def test_display_hotel_success(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        hotel = Hotel.display_hotel("H1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, "H1")

    def test_display_hotel_not_found(self):
        result = Hotel.display_hotel("NONEXISTENT")
        self.assertIsNone(result)

    # --- modify_hotel ---
    def test_modify_hotel_name(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        result = Hotel.modify_hotel("H1", name="Luxury Hotel")
        self.assertTrue(result)
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.name, "Luxury Hotel")

    def test_modify_hotel_location(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        Hotel.modify_hotel("H1", location="Los Angeles")
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.location, "Los Angeles")

    def test_modify_hotel_total_rooms(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        Hotel.modify_hotel("H1", total_rooms=100)
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.total_rooms, 100)
        self.assertEqual(hotel.available_rooms, 100)

    def test_modify_hotel_not_found(self):
        result = Hotel.modify_hotel("NONEXISTENT", name="X")
        self.assertFalse(result)

    # --- reserve_room ---
    def test_reserve_room_success(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        result = Hotel.reserve_room("H1", "R1")
        self.assertTrue(result)
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.available_rooms, 49)
        self.assertIn("R1", hotel.reservations)

    def test_reserve_room_no_availability(self):
        Hotel.create_hotel("H1", "Tiny Hotel", "NYC", 1)
        Hotel.reserve_room("H1", "R1")
        result = Hotel.reserve_room("H1", "R2")
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        result = Hotel.reserve_room("NONEXISTENT", "R1")
        self.assertFalse(result)

    # --- cancel_room ---
    def test_cancel_room_success(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        Hotel.reserve_room("H1", "R1")
        result = Hotel.cancel_room("H1", "R1")
        self.assertTrue(result)
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.available_rooms, 50)

    def test_cancel_room_not_found(self):
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 50)
        result = Hotel.cancel_room("H1", "NONEXISTENT")
        self.assertFalse(result)

    def test_cancel_room_hotel_not_found(self):
        result = Hotel.cancel_room("NONEXISTENT", "R1")
        self.assertFalse(result)

    # --- error handling ---
    def test_load_hotels_corrupt_file(self):
        with open(HOTELS_FILE, "w", encoding="utf-8") as f:
            f.write("INVALID JSON{{{")
        hotels = Hotel._load_hotels()
        self.assertEqual(hotels, {})

    def test_load_hotels_invalid_record(self):
        data = {"H1": {"bad_key": "bad_value"}}
        with open(HOTELS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        hotels = Hotel._load_hotels()
        self.assertEqual(hotels, {})

    def test_to_dict_from_dict(self):
        hotel = Hotel("H1", "Test", "City", 10)
        d = hotel.to_dict()
        hotel2 = Hotel.from_dict(d)
        self.assertEqual(hotel2.hotel_id, "H1")
        self.assertEqual(hotel2.name, "Test")


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class."""

    def setUp(self):
        remove_test_files()

    def tearDown(self):
        remove_test_files()

    # --- create_customer ---
    def test_create_customer_success(self):
        customer = Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice")

    def test_create_customer_duplicate(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        result = Customer.create_customer("C1", "Bob", "bob@mail.com", "555-5678")
        self.assertIsNone(result)

    def test_create_customer_persists(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        self.assertTrue(os.path.exists(CUSTOMERS_FILE))

    # --- delete_customer ---
    def test_delete_customer_success(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        result = Customer.delete_customer("C1")
        self.assertTrue(result)

    def test_delete_customer_not_found(self):
        result = Customer.delete_customer("NONEXISTENT")
        self.assertFalse(result)

    # --- display_customer ---
    def test_display_customer_success(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        customer = Customer.display_customer("C1")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.email, "alice@mail.com")

    def test_display_customer_not_found(self):
        result = Customer.display_customer("NONEXISTENT")
        self.assertIsNone(result)

    # --- modify_customer ---
    def test_modify_customer_name(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        result = Customer.modify_customer("C1", name="Alicia")
        self.assertTrue(result)
        customer = Customer.display_customer("C1")
        self.assertEqual(customer.name, "Alicia")

    def test_modify_customer_email(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        Customer.modify_customer("C1", email="new@mail.com")
        customer = Customer.display_customer("C1")
        self.assertEqual(customer.email, "new@mail.com")

    def test_modify_customer_phone(self):
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")
        Customer.modify_customer("C1", phone="999-9999")
        customer = Customer.display_customer("C1")
        self.assertEqual(customer.phone, "999-9999")

    def test_modify_customer_not_found(self):
        result = Customer.modify_customer("NONEXISTENT", name="X")
        self.assertFalse(result)

    # --- error handling ---
    def test_load_customers_corrupt_file(self):
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            f.write("NOT JSON")
        customers = Customer._load_customers()
        self.assertEqual(customers, {})

    def test_load_customers_invalid_record(self):
        data = {"C1": {"incomplete": True}}
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        customers = Customer._load_customers()
        self.assertEqual(customers, {})

    def test_to_dict_from_dict(self):
        customer = Customer("C1", "Alice", "a@b.com", "123")
        d = customer.to_dict()
        customer2 = Customer.from_dict(d)
        self.assertEqual(customer2.customer_id, "C1")
        self.assertEqual(customer2.name, "Alice")


class TestReservation(unittest.TestCase):
    """Test cases for the Reservation class."""

    def setUp(self):
        remove_test_files()
        Hotel.create_hotel("H1", "Grand Inn", "NYC", 5)
        Customer.create_customer("C1", "Alice", "alice@mail.com", "555-1234")

    def tearDown(self):
        remove_test_files()

    # --- create_reservation ---
    def test_create_reservation_success(self):
        res = Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        self.assertIsNotNone(res)
        self.assertEqual(res.reservation_id, "R1")

    def test_create_reservation_duplicate(self):
        Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        result = Reservation.create_reservation("R1", "C1", "H1", "2024-02-01", "2024-02-05")
        self.assertIsNone(result)

    def test_create_reservation_invalid_customer(self):
        result = Reservation.create_reservation("R1", "INVALID_C", "H1", "2024-01-01", "2024-01-05")
        self.assertIsNone(result)

    def test_create_reservation_invalid_hotel(self):
        result = Reservation.create_reservation("R1", "C1", "INVALID_H", "2024-01-01", "2024-01-05")
        self.assertIsNone(result)

    def test_create_reservation_reduces_availability(self):
        Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.available_rooms, 4)

    def test_create_reservation_persists(self):
        Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        self.assertTrue(os.path.exists(RESERVATIONS_FILE))

    # --- cancel_reservation ---
    def test_cancel_reservation_success(self):
        Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        result = Reservation.cancel_reservation("R1")
        self.assertTrue(result)
        hotel = Hotel.display_hotel("H1")
        self.assertEqual(hotel.available_rooms, 5)

    def test_cancel_reservation_not_found(self):
        result = Reservation.cancel_reservation("NONEXISTENT")
        self.assertFalse(result)

    # --- display_reservation ---
    def test_display_reservation_success(self):
        Reservation.create_reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        res = Reservation.display_reservation("R1")
        self.assertIsNotNone(res)
        self.assertEqual(res.customer_id, "C1")

    def test_display_reservation_not_found(self):
        result = Reservation.display_reservation("NONEXISTENT")
        self.assertIsNone(result)

    # --- error handling ---
    def test_load_reservations_corrupt_file(self):
        with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
            f.write("CORRUPT DATA")
        reservations = Reservation._load_reservations()
        self.assertEqual(reservations, {})

    def test_load_reservations_invalid_record(self):
        data = {"R1": {"missing": "fields"}}
        with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        reservations = Reservation._load_reservations()
        self.assertEqual(reservations, {})

    def test_to_dict_from_dict(self):
        res = Reservation("R1", "C1", "H1", "2024-01-01", "2024-01-05")
        d = res.to_dict()
        res2 = Reservation.from_dict(d)
        self.assertEqual(res2.reservation_id, "R1")
        self.assertEqual(res2.hotel_id, "H1")

    def test_no_rooms_available(self):
        Hotel.create_hotel("H_TINY", "Tiny", "LA", 1)
        Reservation.create_reservation("R1", "C1", "H_TINY", "2024-01-01", "2024-01-05")
        result = Reservation.create_reservation("R2", "C1", "H_TINY", "2024-01-06", "2024-01-10")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
