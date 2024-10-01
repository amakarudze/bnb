import pytest

from reservations.models import Guest, Reservation


@pytest.fixture
def reservation(db, room):
    return Reservation.objects.create(
        user=None,
        number_of_adults=None,
        number_of_children=None,
        rooms=None,
        events=None,
        check_in_date=None,
        check_out_date=None,
        total_cost=None,
        paid=None,
        checked_in=None,
        checked_out=None,
    )


@pytest.fixture
def reservations(db, rooms):
    return Reservation.objects.bulk_create(
        [
            Reservation(
                user=None,
                number_of_adults=None,
                number_of_children=None,
                rooms=None,
                events=None,
                check_in_date=None,
                check_out_date=None,
                total_cost=None,
                paid=None,
                checked_in=None,
                checked_out=None,
            )
        ]
    )


@pytest.fixture
def guest_1(db, reservation):
    return Guest.objects.create(reservation=None, full_name=None, adult=None)


@pytest.fixture
def multiple_guests(db, reservation):
    return Guest.objects.bulk_create([])
