import pytest

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def file_data():
    file_data = {"photo": SimpleUploadedFile("bed_1.jpg", b"file data")}
    return file_data


@pytest.fixture
def valid_room_form(db):
    return {
        "name": "Queen Room",
        "description": "A nice room to share.",
        "bed_type": "Single",
        "number_of_beds": 4,
        "room_type": "Queen",
        "bathroom": "Ensuite",
        "room_capacity": 4,
        "price": 500.0,
        "can_be_rented": True,
    }


@pytest.fixture
def valid_room_form_update(db):
    return {
        "name": "Queen Room",
        "description": "A nice room to share.",
        "bed_type": "Single",
        "number_of_beds": 4,
        "room_type": "Queen",
        "bathroom": "Ensuite",
        "room_capacity": 4,
        "price": 800.0,
        "can_be_rented": True,
    }
