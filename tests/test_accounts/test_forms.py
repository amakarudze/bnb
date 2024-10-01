from accounts.forms import LoginForm


def test_missing_email(manager_client, missing_email):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_email)
    assert form.is_valid() is False
    assert form.errors == {"email": ["This field is required."]}


def test_missing_password(manager_client, missing_password):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_password)
    assert form.is_valid() is False
    assert form.errors == {"password": ["This field is required."]}


def test_valid_login_form(valid_login_form, manager_client):
    """Test login with valid details"""
    form = LoginForm(data=valid_login_form)
    assert form.is_valid()
    assert form.errors == {}
