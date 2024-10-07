import pytest

from reservations.models import Guest, Reservation


@pytest.fixture
def reservation(db, room, guest):
    reservation = Reservation.objects.create(
        user=guest,
        number_of_adults=2,
        number_of_children=0,
        check_in_date="2024-10-24",
        check_out_date="2024-10-28",
    )
    reservation.rooms.set([room])
    return reservation


@pytest.fixture
def guest_1(db, reservation):
    return Guest.objects.create(
        reservation=reservation, full_name="Jane Doe", is_adult=True
    )


@pytest.fixture
def guests(db, reservation):
    return Guest.objects.bulk_create(
        [
            Guest(reservation=reservation, full_name="John Doe", is_adult=True),
            Guest(reservation=reservation, full_name="Jane Doe", is_adult=True),
            Guest(reservation=reservation, full_name="Peter Doe", is_adult=False),
            Guest(reservation=reservation, full_name="Jean Doe", is_adult=False),
            Guest(reservation=reservation, full_name="Pierre Doe", is_adult=False),
        ]
    )
