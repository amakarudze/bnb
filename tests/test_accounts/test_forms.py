from accounts.forms import LoginForm
from accounts.forms import CreateStaffForm


def test_missing_email(manager_client, missing_email):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_email)
    assert form.is_valid() is False
    assert form.errors == {"username": ["This field is required."]}


def test_missing_password(manager_client, missing_password):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_password)
    assert form.is_valid() is False
    assert form.errors == {"password": ["This field is required."]}


def test_valid_login_form(valid_login_form, manager_client):
    """Test login with valid details"""
    form = LoginForm(data=valid_login_form)
    # assert form.is_valid()
    assert form.errors == {}


def test_create_staff_form_valid(create_staff_form_valid):
    form = CreateStaffForm(data=create_staff_form_valid)
    assert form.is_valid() is True
    assert form.errors == {}


def test_create_staff_form_invalid_email(create_staff_form_invalid_email):
    form = CreateStaffForm(data=create_staff_form_invalid_email)
    assert form.is_valid() is False
    assert form.errors == {"email": ["This field is required."]}


def test_create_staff_form_invalid_first_name(create_staff_form_invalid_first_name):
    form = CreateStaffForm(data=create_staff_form_invalid_first_name)
    assert form.is_valid() is False
    assert form.errors == {"first_name": ["This field is required."]}


def test_create_staff_form_invalid_last_name(create_staff_form_invalid_last_name):
    form = CreateStaffForm(data=create_staff_form_invalid_last_name)
    assert form.is_valid() is False
    assert form.errors == {"last_name": ["This field is required."]}


def test_create_staff_form_invalid_password(create_staff_form_invalid_password):
    form = CreateStaffForm(data=create_staff_form_invalid_password)
    assert form.is_valid() is False
    assert form.errors == {"password1": ["This field is required."]}
