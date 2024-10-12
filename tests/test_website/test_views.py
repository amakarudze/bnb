import pytest

from django.shortcuts import reverse


def test_home_view_unauthenticated_guest(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_view_unauthenticated_user_reverse(client):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_manager(manager_client):
    response = manager_client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_front_desk_staff(front_desk_client):
    response = front_desk_client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_aunthenticated_guest(guest_client):
    response = guest_client.get(reverse("website:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_make_reservation_view(guest_client, valid_reservation_rooms):
    response = guest_client.get(reverse("website:make_reservation"))
    assert response.status_code == 200
    response = guest_client.post(
        reverse("website:make_reservation"), data=valid_reservation_rooms
    )
    assert response.status_code == 200  # Should redirect upon success
