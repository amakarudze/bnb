from accounts.models import User


def test_create_user_method(guest):
    user = User.objects.get(email=guest.email)
    assert user is not None
    assert user.email == guest.email
    assert not user.is_staff
    assert user.is_active
    assert not user.is_superuser


def test_create_staff_method(front_desk):
    user = User.objects.get(email=front_desk.email)
    assert user is not None
    assert user.email == front_desk.email
    assert user.is_staff
    assert user.is_active
    assert not user.is_superuser


def test_create_superuser_method(manager):
    user = User.objects.get(email=manager.email)
    assert user is not None
    assert user.email == manager.email
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
