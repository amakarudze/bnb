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


def test_user_model_string_representation(manager):
    assert str(manager) == f"{manager.first_name} {manager.last_name}"


def test_userprofile_model_string_representation(guest_profile):
    assert str(guest_profile) == guest_profile.user.get_full_name()
