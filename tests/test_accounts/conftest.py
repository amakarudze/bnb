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
