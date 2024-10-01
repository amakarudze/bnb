import pytest

from django.contrib.auth.models import Group, Permission
from django.test import Client

from accounts.models import User, UserProfile
from events.models import Event
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
    group_permissions = ["add_user", "change_user", "view_user"]
    return group_permissions


@pytest.fixture
def staff_group_permissions():
    """Fixture for front desk staff group to test their level of access within the system."""
    group_permissions = ["change_user", "view_user"]
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
                description=None,
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
