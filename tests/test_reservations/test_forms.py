import pytest

from reservations.forms import ReservationForm, SignUpForm


@pytest.mark.django_db
def test_valid_reservation_form(valid_reservation_rooms):
    form = ReservationForm(data=valid_reservation_rooms)
    # assert form.is_valid()
    assert form.errors == {}


def test_valid_sign_up_form(db, valid_sign_up_form):
    """Test sign-up with valid details"""
    form = SignUpForm(data=valid_sign_up_form)
    assert form.is_valid()
    assert form.errors == {}
