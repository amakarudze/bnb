from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        label="Email Address",
        help_text="Enter a valid email address",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": "name@example.com",
            }
        ),
    )
    password = forms.CharField(
        max_length=100,
        label="Password",
        help_text="Enter your password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "password", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password"]
