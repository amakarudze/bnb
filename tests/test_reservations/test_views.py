from django.urls import reverse

from pytest_django.asserts import assertRedirects


def test_reservations_list_view_guest(guest_client, reservations, reservations_1):
    response = guest_client.get(reverse("reservations:reservations_list"), follow=True)
    assert response.status_code == 200
    assertRedirects(response, reverse("website:home"))


def test_reservations_list_view_front_desk_staff(
    front_desk_client, reservations, reservations_1
):
    response = front_desk_client.get(reverse("reservations:reservations_list"))
    assert response.status_code == 200


def test_reservations_list_view_manager(manager_client, reservations, reservations_1):
    response = manager_client.get(reverse("reservations:reservations_list"))
    assert response.status_code == 200


def test_update_reservation_view_front_desk_staff(
    front_desk_client, reservation, valid_reservation_rooms
):
    response = front_desk_client.get(
        reverse("reservations:update_reservation", args=(reservation.pk,))
    )
    assert response.status_code == 200
    response = front_desk_client.post(
        reverse("reservations:update_reservation", args=(reservation.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302


def test_update_reservation_view_manager(
    manager_client, reservation, valid_reservation_rooms
):
    response = manager_client.get(
        reverse("reservations:update_reservation", args=(reservation.pk,))
    )
    assert response.status_code == 200
    response = manager_client.post(
        reverse("reservations:update_reservation", args=(reservation.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302


def test_dashboard_view_front_desk_staff(
    front_desk_client,
):
    response = front_desk_client.get(reverse("reservations:dashboard"), follow=True)
    assert response.status_code == 200


def test_dashboard_view_manager(
    manager_client,
):
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


def test_reports_view_manager(manager_client):
    response = manager_client.get(reverse("reservations:reports"), follow=True)
    assert response.status_code == 200


def test_search_reports_view_manager(manager_client):
    response = manager_client.get(reverse("reservations:search_reports"), follow=True)
    assert response.status_code == 200
