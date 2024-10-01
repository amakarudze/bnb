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
def sample_room(db):
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
                description="A nice double room.",
                photo="image.jpeg",
                bed_type="Double",
                number_of_beds=2,
                room_type="Double",
                bathroom="Ensuite",
                price=1200.00,
            ),
            Room(
                name="Muuyu",
                description="A nice family room.",
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=2,
                room_type=None,
                bathroom="Ensuite",
                price=1500.00,
            ),
            Room(
                name="Mutondo",
                description=None,
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=2,
                room_type=None,
                bathroom="Ensuite",
                price=1500.00,
            ),
            Room(
                name="Muhacha",
                description=None,
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=None,
                room_type=None,
                bathroom="Ensuite",
                price=None,
            ),
            Room(
                name="Musekesa",
                description=None,
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=None,
                room_type=None,
                bathroom="Shared",
                price=None,
            ),
            Room(
                name="Mupangara",
                description=None,
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=None,
                room_type=None,
                bathroom="Shared",
                price=None,
            ),
            Room(
                name="Mushuku",
                description=None,
                photo="image.jpeg",
                bed_type=None,
                number_of_beds=2,
                room_type=None,
                bathroom="Ensuite",
                price=None,
            ),
            Room(
                name="Muonde",
                description=None,
                photo="image.jpeg",
                bed_type="Single",
                number_of_beds=3,
                room_type="Twin",
                bathroom="Shared",
                price=1200.00,
            ),
        ]
    )


@pytest.fixture
def event(db):
    return Event.objects.create(
        name=None,
        description=None,
        photo=None,
        host=None,
        venue=None,
        start_date=None,
        end_date=None,
        min_participants=None,
        max_participants=None,
        num_participants=None,
        fully_booked=None,
        price=None,
        age_restrictions=None,
        additional_information=None,
    )


@pytest.fixture
def events(db):
    return Event.objects.bulk_create(
        [
            Event(
                name=None,
                description=None,
                photo=None,
                host=None,
                venue=None,
                start_date=None,
                end_date=None,
                min_participants=None,
                max_participants=None,
                num_participants=None,
                fully_booked=None,
                price=None,
                age_restrictions=None,
                additional_information=None,
            ),
            Event(
                name=None,
                description=None,
                photo=None,
                host=None,
                venue=None,
                start_date=None,
                end_date=None,
                min_participants=None,
                max_participants=None,
                num_participants=None,
                fully_booked=None,
                price=None,
                age_restrictions=None,
                additional_information=None,
            ),
            Event(
                name=None,
                description=None,
                photo=None,
                host=None,
                venue=None,
                start_date=None,
                end_date=None,
                min_participants=None,
                max_participants=None,
                num_participants=None,
                fully_booked=None,
                price=None,
                age_restrictions=None,
                additional_information=None,
            ),
            Event(
                name=None,
                description=None,
                photo=None,
                host=None,
                venue=None,
                start_date=None,
                end_date=None,
                min_participants=None,
                max_participants=None,
                num_participants=None,
                fully_booked=None,
                price=None,
                age_restrictions=None,
                additional_information=None,
            ),
            Event(
                name=None,
                description=None,
                photo=None,
                host=None,
                venue=None,
                start_date=None,
                end_date=None,
                min_participants=None,
                max_participants=None,
                num_participants=None,
                fully_booked=None,
                price=None,
                age_restrictions=None,
                additional_information=None,
            ),
        ]
    )


@pytest.fixture
def guest_profile(db):
    return UserProfile.objects.create(
        user=None,
        address=None,
        city=None,
        postal_code=None,
        state="",
        country="SE",
        phone_number="",
    )
