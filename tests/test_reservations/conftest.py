import pytest


@pytest.fixture
def valid_sign_up_form(db):
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
    }
    return form
