import pytest


@pytest.fixture
def valid_login_form(db, guest):
    form = {"username": "elsa@test.com", "password": "pass1234"}
    return form


@pytest.fixture
def missing_email(db):
    form = {"username": "", "password": "pass1234"}
    return form


@pytest.fixture
def missing_password(db):
    form = {"username": "test@123.com", "password": ""}
    return form


@pytest.fixture
def create_staff_form_valid(db):
    """Fixture for creating user for all valid fields."""
    form = {
        "email": "john@test-server.com",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "pass1234",
        "password2": "pass1234",
    }
    return form


@pytest.fixture
def create_staff_form_invalid_email(db):
    """Fixture for creating user for invalid email field."""
    form = {
        "email": "",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "pass1234",
        "password2": "pass1234",
    }
    return form


@pytest.fixture
def create_staff_form_invalid_first_name(db):
    """Fixture for creating user for  invalid first name fields."""
    form = {
        "email": "john@test-server.com",
        "first_name": "",
        "last_name": "Doe",
        "password1": "pass1234",
        "password2": "pass1234",
    }
    return form


@pytest.fixture
def create_staff_form_invalid_last_name(db):
    """Fixture for creating user for invalid last name."""
    form = {
        "email": "john@test-server.com",
        "first_name": "John",
        "last_name": "",
        "password1": "pass1234",
        "password2": "pass1234",
    }
    return form


@pytest.fixture
def create_staff_form_invalid_password(db):
    """Fixture for creating user for invalid password."""
    form = {
        "email": "john@test-server.com",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "",
        "password2": "pass1234",
    }
    return form


@pytest.fixture
def missing_first_name(db):
    form = {
        "first_name": "",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "dob": "1990-01-01",
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",
        "phone_number": "123-456-7890",
    }
    return form


@pytest.fixture
def missing_last_name(db):
    form = {
        "first_name": "John",
        "last_name": "",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "dob": "1990-01-01",
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",
        "phone_number": "123-456-7890",
    }
    return form


@pytest.fixture
def invalid_sign_up_form_existing_email(db):
    form = {
        "first_name": "Elsa",
        "last_name": "Doe",
        "email": "elsa@test.com",
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
