# Create your tests here.
from django.urls import reverse


def test_valid_login(manager_client, valid_login_form, client):
    """Test login with valid credentials"""
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    response = client.post(reverse("accounts:login"), data=valid_login_form)
    # Check that the login was successful (e.g., redirect or success message)
    assert response.status_code == 302


def test_create_staff_by_manager(manager_client):
    response = manager_client.get(reverse("accounts:create_staff"))
    assert response.status_code == 200


def test_create_staff_by_guest(guest_client):
    response = guest_client.get(reverse("accounts:create_staff"))
    assert response.status_code == 403

# New tests for the sign-up view
def test_sign_up_view_get(client):
    """Test the sign-up view responds to GET requests"""
    response = client.get(reverse("accounts:signup"))  # URL 
    assert response.status_code == 200
    assert "Sign Up" in str(response.content)  # Check if the response contains "Sign Up"


def test_sign_up_view_post_valid(client, valid_sign_up_form):
    """Test sign-up view with valid data"""
    response = client.post(reverse("accounts:signup"), data=valid_sign_up_form)
    assert response.status_code == 302  # Check for redirect on success
    assert response.url == reverse("accounts:login")  # redirect URL 


def test_sign_up_view_post_invalid(client, missing_email):
    """Test sign-up view with invalid data"""
    response = client.post(reverse("accounts:signup"), data=missing_email)
    assert response.status_code == 200  # Should return to the sign-up page
    assert "This field is required." in str(response.content)  # Check for error message