<<<<<<< HEAD
from accounts.forms import LoginForm, SignUpForm
=======
from accounts.forms import LoginForm
from accounts.forms import CreateStaffForm
>>>>>>> a50589a3cc94bfe63d93cab94fb15b97633a4ad0


def test_missing_email(manager_client: Any, missing_email: dict[str, str]):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_email)
    assert form.is_valid() is False
    assert form.errors == {"username": ["This field is required."]}


def test_missing_password(manager_client: Any, missing_password: dict[str, str]):
    """Test login with invalid credentials"""
    form = LoginForm(data=missing_password)
    assert form.is_valid() is False
    assert form.errors == {"password": ["This field is required."]}


def test_valid_login_form(valid_login_form: dict[str, str], manager_client: Any):
    """Test login with valid details"""
    form = LoginForm(data=valid_login_form)
    # assert form.is_valid()
    assert form.errors == {}

<<<<<<< HEAD
# New tests for SignUpForm
def test_missing_first_name(db: None, missing_first_name: dict[str, str]):
    """Test sign-up with missing first name"""
    form = SignUpForm(data=missing_first_name)
=======

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
>>>>>>> a50589a3cc94bfe63d93cab94fb15b97633a4ad0
    assert form.is_valid() is False
    assert form.errors == {"first_name": ["This field is required."]}


<<<<<<< HEAD
def test_missing_last_name(db: None, missing_last_name: dict[str, str]):
    """Test sign-up with missing last name"""
    form = SignUpForm(data=missing_last_name)
=======
def test_create_staff_form_invalid_last_name(create_staff_form_invalid_last_name):
    form = CreateStaffForm(data=create_staff_form_invalid_last_name)
>>>>>>> a50589a3cc94bfe63d93cab94fb15b97633a4ad0
    assert form.is_valid() is False
    assert form.errors == {"last_name": ["This field is required."]}


<<<<<<< HEAD
def test_valid_sign_up_form(db: None, valid_sign_up_form: dict[str, str]):
    """Test sign-up with valid details"""
    form = SignUpForm(data=valid_sign_up_form)
    assert form.is_valid()
    assert form.errors == {}
=======
def test_create_staff_form_invalid_password(create_staff_form_invalid_password):
    form = CreateStaffForm(data=create_staff_form_invalid_password)
    assert form.is_valid() is False
    assert form.errors == {"password1": ["This field is required."]}
>>>>>>> a50589a3cc94bfe63d93cab94fb15b97633a4ad0
