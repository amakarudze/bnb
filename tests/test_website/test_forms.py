import pytest
from reservations.forms import ReservationForm


@pytest.mark.django_db
def test_valid_reservation_form(valid_reservation_rooms):
    form = ReservationForm(data=valid_reservation_rooms)
    # assert form.is_valid()
    assert form.errors == {}


@pytest.mark.django_db
def test_invalid_reservation_form_missing_check_in_date(
    invalid_reservation_missing_check_in_date,
):
    # Remove check_in_date to simulate missing field
    form = ReservationForm(data=invalid_reservation_missing_check_in_date)
    assert not form.is_valid()
    assert form.errors == {"check_in_date": ["This field is required."]}


@pytest.mark.django_db
def test_invalid_reservation_form_missing_rooms(invalid_reservation_missing_rooms):
    # Simulate missing room selection
    form = ReservationForm(data=invalid_reservation_missing_rooms)
    assert not form.is_valid()
    assert form.errors == {"rooms": ["This field is required."]}
