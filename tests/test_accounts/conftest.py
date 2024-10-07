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
