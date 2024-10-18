import pytest

from django.urls import reverse

from django.contrib.auth.models import User


def test_reservations_list_view_guest(guest_client, reservations, reservations_1):
    pass


def test_reservations_list_view_front_desk_staff(
    front_desk_client, reservations, reservations_1
):
    pass


def test_reservations_list_view_manager(manager_client, reservations, reservations_1):
    pass


def test_update_reservation_view_guest(
    guest_client, reservation, valid_reservation_rooms
):
    pass


def test_update_reservation_view_front_desk_staff(
    front_desk_client, reservation, valid_reservation_rooms
):
    pass


def test_update_reservation_view_manager(
    manager_client, reservation, valid_reservation_rooms
):
    pass


def test_dashboard_view_guest(guest_client):
    pass


def test_dashboard_view_front_desk_staff(
    front_desk_client,
):
    pass


def test_dashboard_view_manager(
    manager_client,
):
    pass


def test_add_reservation_view_front_desk_staff(client, add_reservation_valid, guest_formset_valid):
    # response = client.post(reverse("reservations:add_reservation"), data=valid_sign_up_form)
    # assert response.status_code == 302
    # response = client.post(reverse("reservations:add_reservation"), data=valid_sign_up_form)
    # assert response.status_code == 200
    response = client.post(reverse("reservations:add_reservation"), data=add_reservation_valid)
    assert response.status_code == 302
    for index, guest in enumerate(guest_formset_valid):
        form_data[f'guest_set-{index}-full_name'] = guest["full_name"]
        form_data[f'guest_set-{index}-is_adult'] = guest["is_adult"]
        form_data[f'guest_set-{index}-id'] = ''
    
    form_data["guest_set-TOTAL_FORMS"] = str(len(guest_formset_valid))
    form_data["guest_set-INITIAL_FORMS"] = '0'
    form_data["guest_set-MIN_NUM_FORMS"] = '0'
    form_data["guest_set-MAX_NUM_FORMS"] = '1000'

    guests = Guest.objects.filter(reservation=reservation)
    assert guests.count() == len(guest_formset_valid)

    # Check the details of each guest
    for index, guest_data in enumerate(guest_formset_valid):
        guest = guests[index]
        assert guest.full_name == guest_data["full_name"]
        assert guest.is_adult == guest_data["is_adult"]
