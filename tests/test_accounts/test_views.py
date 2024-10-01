# Create your tests here.
from django.urls import reverse


def test_valid_login(manager_client, valid_login_form, client):
    """Test login with valid credentials"""
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    response = client.post(reverse("accounts:login"), data=valid_login_form)
    # Check that the login was successful (e.g., redirect or success message)
    assert response.status_code == 200
