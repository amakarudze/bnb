from django.test import RequestFactory
from django.urls import reverse

from pytest_django.asserts import assertRedirects

from reservations.views import add_reservation


def test_reservations_list_view_guest(guest_client, reservations):
    response = guest_client.get(reverse("reservations:reservations_list"), follow=True)
    assert response.status_code == 200
    assertRedirects(response, reverse("website:home"))


def test_reservations_list_view_front_desk_staff(front_desk_client, reservations):
    response = front_desk_client.get(reverse("reservations:reservations_list"))
    assert response.status_code == 200


def test_reservations_list_view_manager(manager_client, reservations):
    response = manager_client.get(reverse("reservations:reservations_list"))
    assert response.status_code == 200


def test_edit_reservation_view_front_desk_staff(
    front_desk_client, reservation, valid_reservation_rooms
):
    response = front_desk_client.get(
        reverse("reservations:edit_reservation", args=(reservation.pk,))
    )
    assert response.status_code == 200
    response = front_desk_client.post(
        reverse("reservations:edit_reservation", args=(reservation.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302


def test_edit_reservation_view_manager(
    manager_client, reservation, valid_reservation_rooms
):
    response = manager_client.get(
        reverse("reservations:edit_reservation", args=(reservation.pk,))
    )
    assert response.status_code == 200
    response = manager_client.post(
        reverse("reservations:edit_reservation", args=(reservation.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302


def test_dashboard_view_front_desk_staff(front_desk_client):
    response = front_desk_client.get(reverse("reservations:dashboard"), follow=True)
    assert response.status_code == 200


def test_dashboard_view_manager(manager_client):
    response = manager_client.get(reverse("reservations:dashboard"), follow=True)
    assert response.status_code == 200


def test_reports_view_guest(guest_client):
    response = guest_client.get(reverse("reservations:reports"), follow=True)
    assert response.status_code == 200
    assertRedirects(response, reverse("website:home"))


def test_reports_view_staff(front_desk_client):
    response = front_desk_client.get(reverse("reservations:reports"), follow=True)
    assert response.status_code == 200
    assertRedirects(response, reverse("website:home"))


def test_search_reports_view_manager(manager_client):
    response = manager_client.get(reverse("reservations:search_reports"), follow=True)
    assert response.status_code == 200


def test_edit_reservation_view_get(client, reservation):
    """Test GET request for edit_reservation view."""
    response = client.get(
        reverse("reservations:edit_reservation", args=[reservation.id])
    )
    assert response.status_code == 302


def test_edit_reservation_view_post_valid(client, modify_reservation, reservation):
    """Test POST request for valid data in edit_reservation view."""
    response = client.post(
        reverse("reservations:edit_reservation", args=[reservation.id]),
        date=modify_reservation,
    )
    assert reservation.number_of_adults == 2
    assert reservation.number_of_children == 0
    assert response.status_code == 302


def test_edit_reservation_view_cancelled(client, cancel_reservation, reservation):
    """Test POST request for cancelling a reservation."""
    response = client.post(
        reverse("reservations:edit_reservation", args=[reservation.id]),
        data=cancel_reservation,
    )
    assert response.status_code == 302


def test_add_reservation_view_front_desk_staff(
    db,
    front_desk,
    add_reservation_valid,
    guests_group,
    check_in_date,
    check_out_date,
    number_of_adults,
    number_of_children,
    available_rooms,
    upcoming_events,
):
    factory = RequestFactory()
    request = factory.get(reverse("reservations:add_reservation"))
    request.session = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_adults": number_of_adults,
        "number_of_children": number_of_children,
        "rooms": available_rooms,
        "events": upcoming_events,
    }
    request.user = front_desk
    response = add_reservation(request)

    assert response.status_code == 200

    request = factory.post(
        reverse("reservations:add_reservation"), data=add_reservation_valid
    )
    request.session = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_adults": number_of_adults,
        "number_of_children": number_of_children,
        "rooms": available_rooms,
        "events": upcoming_events,
    }
    request.user = front_desk
    response = add_reservation(request)
    assert response.status_code == 200


def test_add_reservation_view_manager(
    db,
    manager,
    add_reservation_valid,
    guests_group,
    check_in_date,
    check_out_date,
    number_of_adults,
    number_of_children,
    available_rooms,
    upcoming_events,
):
    factory = RequestFactory()
    request = factory.get(reverse("reservations:add_reservation"))
    request.session = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_adults": number_of_adults,
        "number_of_children": number_of_children,
        "rooms": available_rooms,
        "events": upcoming_events,
    }
    request.user = manager
    response = add_reservation(request)

    assert response.status_code == 200

    request = factory.get(
        reverse("reservations:add_reservation"), data=add_reservation_valid
    )
    request.session = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_adults": number_of_adults,
        "number_of_children": number_of_children,
        "rooms": available_rooms,
        "events": upcoming_events,
    }
    request.user = manager
    response = add_reservation(request)

    assert response.status_code == 200
