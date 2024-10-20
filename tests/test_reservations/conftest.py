import pytest


@pytest.fixture
def search_report_form(db):
    return {
        "start_date": "2020-10-24",
        "end_date": "2020-10-29",
    }


@pytest.fixture
def add_reservation_valid(db, room):
    form = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "dob": "1990-01-01",  #  date format
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",  #  country code
        "phone_number": "123-456-7890",
        "number_of_adults": 3,
        "number_of_children": 3,
        "check_in_date": "2024-12-01",
        "check_out_date": "2024-12-03",
        "rooms": [room.id],
    }
    return form


@pytest.fixture
def cancel_reservation(db, guest, event, room):
    """Fixture for creating a test reservation."""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "2024-12-15",
        "check_out_date": "2024-12-18",
        "rooms": [room.id],
        "events": [event.id],
        "is_paid": False,
        "is_cancelled": True,
        "is_checked_in": False,
        "is_checked_out": False,
    }


@pytest.fixture
def modify_reservation(db, event, room, guest):
    """Fixture where rooms are missing"""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "2024-12-15",
        "check_out_date": "2024-12-18",
        "rooms": [room.id],
        "events": [event.id],
        "is_paid": True,
        "is_cancelled": False,
        "is_checked_in": True,
        "is_checked_out": False,
    }
