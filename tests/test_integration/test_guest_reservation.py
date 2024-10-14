from django.conf import settings
from django.core import mail
from django.urls import reverse

from pytest_django.asserts import assertRedirects

from accounts.views import send_email


def test_guest_reservation_process(
    db,
    client,
    reservations_1,
    rooms,
    search_form_valid,
    room,
    valid_sign_up_form,
    guest,
    valid_reservation_rooms,
):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200

    response = client.get(reverse("website:search"), data=search_form_valid)
    assert response.status_code == 200
    assert "rooms" in response.context
    assert len(response.context["rooms"]) != len(rooms)
    assert len(response.context["rooms"]) == 6

    response = client.get(reverse("website:make_reservation", args=(room.pk,)))
    assert response.status_code == 302
    assertRedirects(response, f"/accounts/login/?next=/make_reservation/{room.pk}/")

    response = client.get(reverse("accounts:signup"))
    assert response.status_code == 200
    response = client.post(reverse("accounts:signup"), data=valid_sign_up_form)

    to_email = [guest.email]
    send_email(
        "Sign Up Confirmation",
        "Test signup confirmation.",
        settings.DEFAULT_FROM_EMAIL,
        to_email,
    )
    assert len(mail.outbox) == 2
    assert mail.outbox[0].subject, "Signup Confirmation"

    assert response.status_code == 302
    assertRedirects(response, "/")

    client.force_login(guest)
    response = client.get(reverse("website:make_reservation", args=(room.pk,)))
    assert response.status_code == 200
    response = client.post(
        reverse("website:make_reservation", args=(room.pk,)),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 200
