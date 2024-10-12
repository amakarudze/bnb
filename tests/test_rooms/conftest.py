import pytest

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def files():
    image = SimpleUploadedFile("bed_1.jpg", b"file_content", content_type="image/jpeg")
    files = {"photo": image}
    return files


@pytest.fixture
def valid_room_form(db):
    return {
        "name": "Queen Room",
        "description": "A nice room to share.",
        "photo": "image.jpeg",
        "bed_type": "Single",
        "number_of_beds": 4,
        "room_type": "Queen",
        "bathroom": "Ensuite",
        "room_capacity": 4,
        "price": 500.0,
    }


@pytest.fixture
def valid_room_form_update(db):
    return {
        "name": "Queen Room",
        "description": "A nice room to share.",
        "photo": "image.jpeg",
        "bed_type": "Single",
        "number_of_beds": 4,
        "room_type": "Queen",
        "bathroom": "Ensuite",
        "room_capacity": 4,
        "price": 800.0,
    }
