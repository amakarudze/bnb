import pytest

from datetime import date

from django.contrib.auth.models import Group, Permission
from django.test import Client

from accounts.models import User, UserProfile
from events.models import Event
from reservations.models import Guest, Reservation

from rooms.models import Room


def add_permissions(user, group, group_permissions):
    user.groups.add(group)
    user.save()
    user.refresh_from_db()
    for perm in group_permissions:
        permission = Permission.objects.get(codename=perm)
        user.user_permissions.add(permission)
    user = User.objects.get(id=user.id)
    return user


@pytest.fixture
def client(db):
    """Fixture for client to be used for all unauthenticated users/guests who use the BnB website."""
    client = Client()
    return client


@pytest.fixture
def guests_group(db):
    """Fixture for guests group to be used to assign test guest users to the group to test their level of access and functionality."""
    group = Group.objects.create(name="Guests")
    return group


@pytest.fixture
def staff_group(db):
    """Fixture for staff group to be used to assign test front desk staff to test their level of access and functionality."""
    group = Group.objects.create(name="Staff")
    return group


@pytest.fixture
def guests_group_permissions():
    """Fixture for guest group permissions to test their level of access within the system."""
    group_permissions = [
        "add_user",
        "change_user",
        "view_user",
        "add_userprofile",
        "change_userprofile",
        "view_userprofile",
        "add_reservation",
        "change_reservation",
        "view_reservation",
    ]
    return group_permissions


@pytest.fixture
def staff_group_permissions():
    """Fixture for front desk staff group to test their level of access within the system."""
    group_permissions = [
        "add_user",
        "change_user",
        "view_user",
        "add_room",
        "change_room",
        "view_room",
        "add_event",
        "change_event",
        "view_event",
        "add_reservation",
        "change_reservation",
        "view_reservation",
        "add_userprofile",
        "change_userprofile",
        "view_userprofile",
    ]
    return group_permissions


@pytest.fixture
def guest(db, guests_group, guests_group_permissions):
    """Fixture to create a guest user."""
    user = User.objects.create_user(
        email="elsa@test.com", first_name="Elsa", last_name="Doe", password="pass1234"
    )
    return add_permissions(user, guests_group, guests_group_permissions)


@pytest.fixture
def front_desk(db, staff_group, staff_group_permissions):
    """Fixture to create a front desk staff user."""
    user = User.objects.create_staff(
        email="elias@test.com", first_name="Elias", last_name="Doe", password="pass1234"
    )
    return add_permissions(user, staff_group, staff_group_permissions)


@pytest.fixture
def manager(db):
    """Fixture to create a manager/admin user."""
    user = User.objects.create_superuser(
        email="carl@test.com", first_name="Carl", last_name="Doe", password="pass1234"
    )
    return user


@pytest.fixture
def guest_client(client, guest):
    """Fixture to create a client to simulate what a guest can view when browsing the website."""
    client.force_login(guest)
    return client


@pytest.fixture
def front_desk_client(client, front_desk):
    """Fixture to create a client to simulate what front desk staff can view while browsing the website."""
    client.force_login(front_desk)
    return client


@pytest.fixture
def manager_client(client, manager):
    """
    Fixture to create a client to simulate what the manager/admin can do while browsing the website.
    This user should be able to access everything.
    """
    client.force_login(manager)
    return client


@pytest.fixture
def room(db):
    return Room.objects.create(
        name="Acacia",
        description="A nice single room.",
        photo="image.jpeg",
        bed_type="Double",
        number_of_beds=1,
        room_type="Single",
        bathroom="Shared",
        price=1000.00,
    )


@pytest.fixture
def rooms(db):
    return Room.objects.bulk_create(
        [
            Room(
                name="Baobab",
                description="A nice queen room.",
                photo="image.jpeg",
                bed_type="Queen",
                number_of_beds=2,
                room_type="Queen",
                bathroom="Ensuite",
                price=1200.00,
            ),
            Room(
                name="Muuyu",
                description="A nice family room.",
                photo="image.jpeg",
                bed_type="Queen",
                number_of_beds=4,
                room_type="Family",
                bathroom="Ensuite",
                price=2500.00,
            ),
            Room(
                name="Mutondo",
                description="A nice double room",
                photo="image.jpeg",
                bed_type="Double",
                number_of_beds=2,
                room_type="Double",
                bathroom="Ensuite",
                price=1500.00,
            ),
            Room(
                name="Muhacha",
                description="A nice and cosy twin room.",
                photo="image.jpeg",
                bed_type="Three Quarter",
                number_of_beds=2,
                room_type="Double/Twin",
                bathroom="Shared",
                price=1500.00,
            ),
            Room(
                name="Musekesa",
                description="A nice family room.",
                photo="image.jpeg",
                bed_type="Queen",
                number_of_beds=4,
                room_type="Family",
                bathroom="Ensuite",
                price=2500,
            ),
            Room(
                name="Mupangara",
                description="A nice executive room.",
                photo="image.jpeg",
                bed_type="King",
                number_of_beds=1,
                room_type="Executive",
                bathroom="Ensuite",
                price=1800.00,
            ),
            Room(
                name="Mushuku",
                description="A nice honeymoon suite.",
                photo="image.jpeg",
                bed_type="King",
                number_of_beds=1,
                room_type="Honeymoon Suite",
                bathroom="Ensuite",
                price=2000.00,
            ),
            Room(
                name="Muonde",
                description="A nice single room",
                photo="image.jpeg",
                bed_type="Single",
                number_of_beds=3,
                room_type="Double/Twin",
                bathroom="Shared",
                price=1200.00,
            ),
        ]
    )


@pytest.fixture
def event(db):
    return Event.objects.create(
        name="Arts and Crafts",
        description="An arts and crafts activity for children below 12 years.",
        photo="image.jpeg",
        host="Jane Doe",
        venue="Mutamba Room",
        start_date="2024-10-30 09:00",
        end_date="2024-10-30 13:00",
        min_participants=6,
        max_participants=15,
        num_participants=3,
        fully_booked=False,
        price=0,
        age_restrictions="Below 12 years",
        additional_information="All materials are provided. Snacks are also provided.",
    )


@pytest.fixture
def events(db):
    return Event.objects.bulk_create(
        [
            Event(
                name="Over 60s Night",
                description="A night of fun for the over 60s.",
                photo="image.jpeg",
                host="BnB",
                venue="Musasa Room",
                start_date="2024-10-30 20:00",
                end_date="2024-10-31 00:00",
                min_participants=10,
                max_participants=20,
                num_participants=12,
                fully_booked=False,
                price=0,
                age_restrictions="60 years+",
                additional_information="A night of Karaoke and dancing.",
            ),
            Event(
                name="Guided City Tour",
                description="A guided tour of the city and town square.",
                photo="image.jpeg",
                host="Karlskrona Municipality",
                venue="Karlskrona Town Square",
                start_date="2024-10-30 20:00",
                end_date="2024-10-31 00:00",
                min_participants=10,
                max_participants=20,
                num_participants=12,
                fully_booked=False,
                price=0,
                age_restrictions="No age restrictions",
                additional_information="An activity for the whole family.",
            ),
        ]
    )


@pytest.fixture
def guest_profile(db, guest):
    return UserProfile.objects.create(
        user=guest,
        dob="2004-11-05",
        address=" 20 Some Nice Road",
        city="Karlskrona",
        postal_code=37141,
        state="",
        country="SE",
        phone_number="+46760812456",
    )


@pytest.fixture
def guest2(db, guests_group, guests_group_permissions):
    """Fixture to create a guest user."""
    user = User.objects.create_user(
        email="elsa@test-server.com",
        first_name="Elsa",
        last_name="Doe",
        password="pass1234",
    )
    return add_permissions(user, guests_group, guests_group_permissions)


@pytest.fixture
def guest2_profile(db, guest):
    return UserProfile.objects.create(
        user=guest,
        dob="1991-05-11",
        address=" 20 Some Nice Road",
        city="Karlskrona",
        postal_code=37141,
        state="",
        country="SE",
        phone_number="+46760812456",
    )


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
def valid_reservation_event_and_rooms(db, event, room, guest):
    """Fixture where rooms are missing"""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "2024-12-15",
        "check_out_date": "2024-12-18",
        "rooms": [room.id],
        "events": [event.id],
    }


@pytest.fixture
def valid_reservation_rooms(db, room, guest):
    """Fixture where rooms are missing"""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "2024-12-10",
        "check_out_date": "2024-12-12",
        "rooms": [room.id],
    }


@pytest.fixture
def invalid_reservation_missing_rooms(db, event, guest):
    """Fixture where rooms are missing"""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "2024-12-10",
        "check_out_date": "2024-12-12",
        "rooms": [],  # No rooms selected
    }


@pytest.fixture
def invalid_reservation_missing_check_in_date(db, room, event, guest):
    """Fixture for a reservation missing the required check_in_date"""
    return {
        "user": guest,
        "number_of_adults": 2,
        "number_of_children": 1,
        "check_in_date": "",  # Missing check_in_date
        "check_out_date": date.today(),
        "rooms": [room.id],
        "events": [event.id],
    }


@pytest.fixture
def reservations(db, guest, guest2, room, events):
    reservation1 = Reservation.objects.create(
        user=guest2,
        number_of_adults=1,
        number_of_children=0,
        check_in_date="2024-12-29",
        check_out_date="2024-12-05",
    )
    reservation1.rooms.set([room])

    reservation2 = Reservation.objects.create(
        user=guest,
        number_of_adults=3,
        number_of_children=3,
        check_in_date="2024-12-28",
        check_out_date="2024-12-02",
    )
    reserved_rooms = Room.objects.filter(room_type="Family")
    reservation2.rooms.set([room.id for room in reserved_rooms])
    reservation2.events.set([event.id for event in events])
    return reservation1, reservation2


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


@pytest.fixture
def reservations_1(db, rooms, guest, guest2, room, events):
    reservation1 = Reservation.objects.create(
        user=guest2,
        number_of_adults=1,
        number_of_children=0,
        check_in_date="2024-10-29",
        check_out_date="2024-11-05",
    )
    reservation1.rooms.set([room.id])
    reservation2 = Reservation.objects.create(
        user=guest,
        number_of_adults=3,
        number_of_children=3,
        check_in_date="2024-10-28",
        check_out_date="2024-11-02",
    )

    reserved_rooms = Room.objects.filter(room_type="Family")
    reservation2.rooms.set([room.id for room in reserved_rooms])
    reservation2.events.set([event.id for event in events])
    return reservation1, reservation2


@pytest.fixture
def search_form_valid():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-11-03",
        "number_of_adults": 1,
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_no_adults():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-11-03",
        "number_of_adults": "",
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_zero_adults():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-11-03",
        "number_of_adults": 0,
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_check_out_same_day():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-10-31",
        "number_of_adults": 2,
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_check_in_date_past():
    return {
        "check_in_date": "2024-10-12",
        "check_out_date": "2024-11-03",
        "number_of_adults": 1,
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_check_out_date_less_than_check_in_date():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-10-29",
        "number_of_adults": 1,
        "number_of_children": 0,
    }


@pytest.fixture
def search_form_invalid_no_children_number():
    return {
        "check_in_date": "2024-10-31",
        "check_out_date": "2024-11-03",
        "number_of_adults": 2,
        "number_of_children": "",
    }


@pytest.fixture
def valid_sign_up_form(db):
    form = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "dob": "1990-01-01",  #  date format
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",  #  country code
        "phone_number": "123-456-7890",
    }
    return form


@pytest.fixture
def search_form_by_booking_code():
    return {
        "booking_code": "ABCDEF",
    }


@pytest.fixture
def guest_formset_valid():
    guest1={
        "full_name": "John Doe",
        "is_adult": True        
    }
    guest2={
        "full_name": "Jane Doe", 
        "is_adult": True
    }
    guest3={
        "full_name": "Jean Doe", 
        "is_adult": True
    }
    return [guest1, guest2, guest3]


@pytest.fixture
def add_reservation_valid(db, room):
    form = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "dob": "1990-01-01",  #  date format
        "address": "123 Main St",
        "city": "Cityville",
        "postal_code": "12345",
        "state": "State",
        "country": "US",  #  country code
        "phone_number": "123-456-7890",
        "number_of_adults": 3,
        "number_of_children": 3,
        "check_in_date": "2024-12-01",
        "check_out_date": "2024-12-03",
        "rooms": [room.id],

    }
