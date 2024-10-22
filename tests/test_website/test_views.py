import pytest

from django.shortcuts import reverse
from django.test import RequestFactory

from pytest_django.asserts import assertRedirects

from website.views import make_reservation


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
def test_make_reservation_view(
    guest_client,
    valid_reservation_rooms,
    room,
    check_in_date,
    check_out_date,
    number_of_adults,
    number_of_children,
    available_rooms,
    upcoming_events,
    guest,
):
    factory = RequestFactory()
    request = factory.get(reverse("website:make_reservation"))
    request.session = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_adults": number_of_adults,
        "number_of_children": number_of_children,
        "rooms": available_rooms,
        "events": upcoming_events,
    }
    request.user = guest
    response = make_reservation(request)
    assert response.status_code == 200

    response = guest_client.post(
        reverse("website:make_reservation"),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302


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


def test_search_view(db, client, reservations, rooms, search_form_valid):
    response = client.get(reverse("website:search"), data=search_form_valid)
    assert response.status_code == 200
    assert "rooms" in response.context
    assert len(response.context["rooms"]) != len(rooms)
    assert len(response.context["rooms"]) == 7


def test_room_details_view(client, room):
    response = client.get(reverse("website:room", args=(room.pk,)))
    assert response.status_code == 200


def test_event_details_view(client, event):
    response = client.get(reverse("website:event", args=(event.pk,)))
    assert response.status_code == 200


def test_reservations_view_guest(guest_client):
    response = guest_client.get(reverse("website:reservations"))
    assert response.status_code == 200


def test_reservations_view_unathenticated_guest(client):
    response = client.get(reverse("website:reservations"), follow=True)
    assert response.status_code == 200
    assertRedirects(response, "/accounts/login/?next=/reservations/")


def test_search_by_booking_code_view(
    db, client, search_form_by_booking_code, reservation
):
    response = client.get(
        reverse("website:search_result_by_booking_code"),
        data=search_form_by_booking_code,
    )
    assert response.status_code == 302
