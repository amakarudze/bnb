import pytest

from reservations.models import Guest, Reservation


@pytest.fixture
def reservation(db, room, guest):
    return Reservation.objects.create(
        user=guest,
        number_of_adults=2,
        number_of_children=0,
        rooms=[room.id],
        events=[],
        check_in_date="2024-10-24",
        check_out_date="2024-10-28",
    )


@pytest.fixture
def reservations(db, rooms, guest, guest2, room, events):
    return Reservation.objects.bulk_create(
        [
            Reservation(
                user=guest2.id,
                number_of_adults=1,
                number_of_children=0,
                rooms=[room.id],
                events=[],
                check_in_date="2024-10-29",
                check_out_date="2024-11-05",
            ),
            Reservation(
                user=guest.id,
                number_of_adults=3,
                number_of_children=3,
                rooms=[room.id for room in rooms if room.room_type == "Family Room"],
                events=[event.id for event in events],
                check_in_date="2024-10-28",
                check_out_date="2024-11-02",
            ),
        ]
    )


@pytest.fixture
def guest_1(db, reservation):
    return Guest.objects.create(
        reservation=reservation.id, full_name="Jane Doe", adult=True
    )


@pytest.fixture
def guests(db, reservation):
    return Guest.objects.bulk_create(
        [
            Guest(reservation=reservation.id, full_name="John Doe", adult=True),
            Guest(reservation=reservation.id, full_name="Jane Doe", adult=True),
            Guest(reservation=reservation.id, full_name="Peter Doe", adult=False),
            Guest(reservation=reservation.id, full_name="Jean Doe", adult=False),
            Guest(reservation=reservation.id, full_name="Pierre Doe", adult=False),
        ]
    )
