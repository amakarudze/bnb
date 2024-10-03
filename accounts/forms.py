from django import forms

from .models import User


from django.contrib.auth import password_validation
from django.contrib.auth.models import Group
from django.forms import ValidationError



class LoginForm(forms.ModelForm):
    email = forms.CharField(
        max_length=100,
        label="Email Address",
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
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "password", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password"]


class CreateStaffForm(forms.ModelForm):
    email = forms.CharField(
        max_length=100,
        label="Staff Email Address:",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": "Email address",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=100,
        label="Staff First Name:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "first_name",
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        label="Staff Last Name:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "last_name",
                "placeholder": "Last name",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=100,
        label="Password:",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password1",
                "placeholder": "Enter Password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=100,
        label="Confirm Password:",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password2",
                "placeholder": "Confirm Password",
            }
        ),
    )
    

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            
        )

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("The two passwords do not match!")
        else:
            password_validation.validate_password(password1)
            return password1
