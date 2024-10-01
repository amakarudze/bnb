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
