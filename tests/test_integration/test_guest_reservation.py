import pytest

from django.conf import settings
from django.core import mail
from django.test import RequestFactory
from django.urls import reverse

from pytest_django.asserts import assertRedirects

from accounts.views import send_email
from website.views import make_reservation


@pytest.mark.transactional_db(True)
def test_guest_reservation_process(
    client,
    guest,
    search_form_valid,
    valid_sign_up_form,
    valid_reservation_rooms,
    reservation,
    reservations,
    room,
    rooms,
    available_rooms,
    check_in_date,
    check_out_date,
    number_of_adults,
    number_of_children,
    upcoming_events,
):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200

    response = client.get(reverse("website:search"), data=search_form_valid)
    assert response.status_code == 200
    assert "rooms" in response.context
    assert len(response.context["rooms"]) == 7

    response = client.get(reverse("website:make_reservation"))
    assert response.status_code == 302
    assertRedirects(response, "/accounts/login/?next=/make_reservation/")

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

    assert response.status_code == 200

    client.force_login(guest)

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

    response = client.post(
        reverse("website:make_reservation"),
        data=valid_reservation_rooms,
    )
    assert response.status_code == 302
