import pytest


@pytest.fixture
def search_report_form(db):
    return {
        "start_date": "2020-10-24",
        "end_date": "2020-10-29",
    }


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
