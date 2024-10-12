import pytest


@pytest.fixture
def valid_login_form(db):
    form = {"email": "acarl@test.com", "password": "pass1234"}
    return form


@pytest.fixture
def missing_email(db):
    form = {"email": "", "password": "pass1234"}
    return form


@pytest.fixture
def missing_password(db):
    form = {"email": "test@123.com", "password": ""}
    return form

@pytest.fixture
def valid_sign_up_form(db):
    form = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "dob": "1990-01-01",  #  date format 
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",  #  country code 
        "phone_number": "123-456-7890"
    }
    return form


@pytest.fixture
def missing_first_name(db):
    form = {
        "first_name": "",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "dob": "1990-01-01",
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",
        "phone_number": "123-456-7890"
    }
    return form


@pytest.fixture
def missing_last_name(db):
    form = {
        "first_name": "John",
        "last_name": "",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "dob": "1990-01-01",
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",
        "phone_number": "123-456-7890"
    }
    return form
