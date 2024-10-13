import pytest

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def file_data():
    file_data = {"photo": SimpleUploadedFile("bed_1.jpg", b"file data")}
    return file_data


@pytest.fixture
def valid_event_form(db):
    return {
        "name": "Concert Day",
        "description": "Concert by Ed Sheeran",
        "host": "Payel",
        "venue": "Multisalen",
        "start_date": "2024-12-05",
        "end_date": "2024-12-06",
        "min_participants": 100,
        "max_participants": 150,
        "num_participants": 130,
        "fully_booked": True,
        "price": 560,
        "age_restrictions": "No age restrictions",
        "additional_information": "No food allowed in concert hall",
    }


@pytest.fixture
def valid_event_form_update(db):
    return {
        "name": "Concert Day",
        "description": "Concert by Ed Sheeran",
        "host": "Anna",
        "venue": "Multisalen",
        "start_date": "2024-12-05",
        "end_date": "2024-12-06",
        "min_participants": 100,
        "max_participants": 150,
        "num_participants": 130,
        "fully_booked": True,
        "price": 560,
        "age_restrictions": "No age restrictions",
        "additional_information": "No food allowed in concert hall",
    }
