import pytest

from django.shortcuts import reverse


@pytest.mark.django_db
def test_make_reservation_view(guest_client, valid_reservation_rooms):
    response = guest_client.get(reverse("reservations:make_reservation"))
    assert response.status_code == 200
    response = guest_client.post(
        reverse("reservations:make_reservation"), data=valid_reservation_rooms
    )
    assert response.status_code == 200


def test_sign_up_staff_for_guest_valid(client, valid_sign_up_form):
    """Test sign-up view with valid data"""
    response = client.post(reverse("reservations:sign-up-for-guest"), data=valid_sign_up_form)
    assert response.status_code == 200
    assert response.url == reverse("reservations:make-reservation")
