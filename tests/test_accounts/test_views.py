import pytest

from django.conf import settings
from django.core import mail
from django.urls import reverse

from accounts.views import send_email

from pytest_django.asserts import assertRedirects

from accounts.models import User


def test_valid_login(manager_client, valid_login_form, client):
    """Test login with valid credentials"""
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    response = client.post(reverse("accounts:login"), data=valid_login_form)
    assert response.status_code == 302


def test_create_staff_by_manager(manager_client):
    response = manager_client.get(reverse("accounts:create_staff"))
    assert response.status_code == 200


def test_create_staff_by_guest(guest_client):
    response = guest_client.get(reverse("accounts:create_staff"))
    assert response.status_code == 403


def test_sign_up_view_get(client):
    """Test the sign-up view responds to GET requests"""
    response = client.get(reverse("accounts:signup"))
    assert response.status_code == 200
    assert "Sign Up" in str(response.content)


@pytest.mark.django_db
def test_sign_up_view_post_valid(client, valid_sign_up_form, guests_group):
    """Test sign-up view with valid data"""
    response = client.post(
        reverse("accounts:signup"), data=valid_sign_up_form, follow=True
    )
    assert response.status_code == 200
    # assertRedirects(response, reverse("website:make_reservation"))
    guest = User.objects.get(email=valid_sign_up_form["email"])
    to_email = [guest.email]
    send_email(
        "Sign Up Confirmation",
        "Test signup confirmation.",
        settings.DEFAULT_FROM_EMAIL,
        to_email,
    )
    assert len(mail.outbox) == 2
    assert mail.outbox[0].subject, "Signup Confirmation"


def test_sign_up_view_post_valid_with_room_to_book(
    client, valid_sign_up_form, guests_group, room
):
    """Test sign-up view with valid data"""
    response = client.post(reverse("accounts:signup"), data=valid_sign_up_form)
    assert response.status_code == 200
    # assert response.url == reverse("website:make_reservation")


def test_sign_up_view_post_invalid(client, missing_email):
    """Test sign-up view with invalid data"""
    response = client.post(reverse("accounts:signup"), data=missing_email)
    assert response.status_code == 200


def test_logout_view(guest_client):
    response = guest_client.post(reverse("accounts:logout"))
    assert response.status_code == 302
    assertRedirects(response, "/")


@pytest.mark.django_db
def test_signup_view_existing_email(client, guest, invalid_sign_up_form_existing_email):
    response = client.post(
        reverse("accounts:signup"),
        data=invalid_sign_up_form_existing_email,
        follow=True,
    )
    assert response.status_code == 200
