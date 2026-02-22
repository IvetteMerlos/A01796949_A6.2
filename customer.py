"""Customer module for the Reservation System."""

import json
import os

CUSTOMERS_FILE = "customers.json"


class Customer:
    """Represents a customer in the reservation system."""

    def __init__(self, customer_id, name, email, phone):
        """Initialize a Customer instance."""
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convert Customer to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @staticmethod
    def from_dict(data):
        """Create a Customer from a dictionary."""
        return Customer(
            data["customer_id"],
            data["name"],
            data["email"],
            data["phone"],
        )

    @staticmethod
    def _load_customers():
        """Load all customers from file."""
        if not os.path.exists(CUSTOMERS_FILE):
            return {}
        try:
            with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            customers = {}
            for k, v in data.items():
                try:
                    customers[k] = Customer.from_dict(v)
                except (KeyError, TypeError) as e:
                    print(f"Error loading customer record '{k}': {e}")
            return customers
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading customers file: {e}")
            return {}

    @staticmethod
    def _save_customers(customers):
        """Save all customers to file."""
        try:
            with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {k: v.to_dict() for k, v in customers.items()}, f, indent=4
                )
        except OSError as e:
            print(f"Error saving customers file: {e}")

    @staticmethod
    def create_customer(customer_id, name, email, phone):
        """Create and persist a new customer."""
        customers = Customer._load_customers()
        if customer_id in customers:
            print(f"Customer '{customer_id}' already exists.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer
        Customer._save_customers(customers)
        print(f"Customer '{name}' created successfully.")
        return customer

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer by ID."""
        customers = Customer._load_customers()
        if customer_id not in customers:
            print(f"Customer '{customer_id}' not found.")
            return False
        del customers[customer_id]
        Customer._save_customers(customers)
        print(f"Customer '{customer_id}' deleted successfully.")
        return True

    @staticmethod
    def display_customer(customer_id):
        """Display customer information."""
        customers = Customer._load_customers()
        if customer_id not in customers:
            print(f"Customer '{customer_id}' not found.")
            return None
        customer = customers[customer_id]
        print(f"Customer ID: {customer.customer_id}")
        print(f"Name       : {customer.name}")
        print(f"Email      : {customer.email}")
        print(f"Phone      : {customer.phone}")
        return customer

    @staticmethod
    def get_all_customers():
        """Return all customers as a dictionary."""
        return Customer._load_customers()

    @staticmethod
    def modify_customer(customer_id, name=None, email=None, phone=None):
        """Modify customer information."""
        customers = Customer._load_customers()
        if customer_id not in customers:
            print(f"Customer '{customer_id}' not found.")
            return False
        customer = customers[customer_id]
        if name:
            customer.name = name
        if email:
            customer.email = email
        if phone:
            customer.phone = phone
        Customer._save_customers(customers)
        print(f"Customer '{customer_id}' modified successfully.")
        return True
