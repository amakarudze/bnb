from datetime import date

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ValidationError

from django_countries.fields import CountryField

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


class SignUpForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Date of Birth",
                "type": "date",
            }
        )
    )
    address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Address"}
        ),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
    )
    postal_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Postal Code"}
        ),
    )
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
    )
    country = CountryField(blank_label="(select country)").formfield()
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Phone Number"}
        ),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({"password": ["Passwords do not match."]})

        dob = cleaned_data.get("dob")
        if (date.today() - dob).days < 18:
            raise forms.ValidationError(
                {"dob": ["You have to be 18 years and above to use our site."]}
            )

        return super().clean()
