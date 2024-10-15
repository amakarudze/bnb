import pytest

from django.shortcuts import reverse


def test_home_view_unauthenticated_guest(client, rooms):
    response = client.get("/")
    assert response.status_code == 200


def test_home_view_unauthenticated_user_reverse(client, rooms):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_manager(manager_client):
    response = manager_client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_front_desk_staff(front_desk_client):
    response = front_desk_client.get(reverse("website:home"))
    assert response.status_code == 200


def test_home_view_aunthenticated_guest(guest_client, rooms):
    response = guest_client.get(reverse("website:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_make_reservation_view(guest_client, valid_reservation_rooms, room):
    response = guest_client.get(reverse("website:make_reservation", args=(room.pk,)))
    assert response.status_code == 200
    response = guest_client.post(
        reverse("website:make_reservation", args=(room.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 200


def test_view_about_us(guest_client):
    response = guest_client.get(reverse("website:about_us"))
    assert response.status_code == 200


def test_view_contact_us(guest_client):
    response = guest_client.get(reverse("website:contact_us"))
    assert response.status_code == 200


def test_rooms_view_unauthenticated_guest(client):
    response = client.get(reverse("website:rooms"))
    assert response.status_code == 200


def test_rooms_view_authenticated_guest(guest_client):
    response = guest_client.get(reverse("website:rooms"))
    assert response.status_code == 200


def test_search_view(db, client, reservations_1, rooms, search_form_valid):
    response = client.get(reverse("website:search"), data=search_form_valid)
    assert response.status_code == 200
    assert "rooms" in response.context
    assert len(response.context["rooms"]) != len(rooms)
    assert len(response.context["rooms"]) == 6


def test_room_details_view(client, room):
    response = client.get(reverse("website:room", args=(room.pk,)))
    assert response.status_code == 200
