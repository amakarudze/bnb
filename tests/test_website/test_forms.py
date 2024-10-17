import pytest

from reservations.forms import ReservationForm
from website.forms import SearchForm, SearchByBookingCodeForm


@pytest.mark.django_db
def test_valid_reservation_form(valid_reservation_rooms):
    form = ReservationForm(data=valid_reservation_rooms)
    assert form.is_valid()
    assert form.errors == {}


@pytest.mark.django_db
def test_invalid_reservation_form_missing_check_in_date(
    invalid_reservation_missing_check_in_date,
):
    form = ReservationForm(data=invalid_reservation_missing_check_in_date)
    assert not form.is_valid()
    assert form.errors == {"check_in_date": ["This field is required."]}


@pytest.mark.django_db
def test_invalid_reservation_form_missing_rooms(invalid_reservation_missing_rooms):
    form = ReservationForm(data=invalid_reservation_missing_rooms)
    assert not form.is_valid()
    assert form.errors == {"rooms": ["This field is required."]}


def test_search_form_invalid_no_adults(search_form_invalid_no_adults):
    form = SearchForm(data=search_form_invalid_no_adults)
    assert not form.is_valid()
    assert form.errors == {"number_of_adults": ["This field is required."]}


def test_search_form_invalid_zero_adults(search_form_invalid_zero_adults):
    form = SearchForm(data=search_form_invalid_zero_adults)
    assert not form.is_valid()
    assert form.errors == {"number_of_adults": ["Number of adult guests cannot be 0."]}


def test_search_form_invalid_no_children_number(search_form_invalid_no_children_number):
    form = SearchForm(data=search_form_invalid_no_children_number)
    assert not form.is_valid()
    assert form.errors == {"number_of_children": ["This field is required."]}


def test_search_form_invalid_check_out_same_day(search_form_invalid_check_out_same_day):
    form = SearchForm(data=search_form_invalid_check_out_same_day)
    assert not form.is_valid()
    assert form.errors == {
        "check_out_date": ["Check out date should be greater than check in date."]
    }


def test_search_form_invalid_check_in_date_past(search_form_invalid_check_in_date_past):
    form = SearchForm(data=search_form_invalid_check_in_date_past)
    assert not form.is_valid()
    assert form.errors == {"check_in_date": ["Check in date cannot be in the past."]}


def test_search_form_invalid_check_out_date_less_than_check_in_date(
    search_form_invalid_check_out_date_less_than_check_in_date,
):
    form = SearchForm(data=search_form_invalid_check_out_date_less_than_check_in_date)
    assert not form.is_valid()
    assert form.errors == {
        "check_out_date": ["Check out date should be greater than check in date."]
    }


def test_search_form_by_booking_code(
    search_form_by_booking_code,
):
    form = SearchByBookingCodeForm(data=search_form_by_booking_code)
    assert form.is_valid()
    assert form.errors == {}
