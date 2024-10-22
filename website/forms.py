from datetime import date

from django import forms
from django.forms import ValidationError


class SearchForm(forms.Form):
    check_in_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id": "check_in_date",
                "class": "form-control mr-sm-2",
                "placeholder": "YYYY-MM-DD",
                "type": "date",
            }
        )
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id": "check_out_date",
                "class": "form-control mr-sm-2",
                "placeholder": "YYYY-MM-DD",
                "type": "date",
            }
        )
    )
    number_of_adults = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "number_of_adults",
                "class": "form-control mr-sm-2",
                "placeholder": "Number of adults",
            }
        )
    )
    number_of_children = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "number_of_children",
                "class": "form-control mr-sm-2",
                "placeholder": "Number of children",
                "required": False,
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")
        number_of_adults = self.cleaned_data.get("number_of_adults")

        if check_in_date < date.today():
            raise ValidationError(
                {"check_in_date": ["Check in date cannot be in the past."]}
            )
        if check_out_date < date.today():
            raise ValidationError(
                {"check_out_date": ["Check out date cannot be in the past."]}
            )
        if check_in_date >= check_out_date:
            raise ValidationError(
                {
                    "check_out_date": [
                        "Check out date should be greater than check in date."
                    ]
                }
            )

        if number_of_adults == 0:
            raise ValidationError(
                {"number_of_adults": ["Number of adult guests cannot be 0."]}
            )
            raise ValidationError("Number of adult guests cannot be 0.")


class SearchByBookingCodeForm(forms.Form):
    booking_code = forms.CharField(
        max_length=6,
        label="Enter Unique Booking Code:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "booking_code",
                "placeholder": "Booking Code",
            }
        ),
    )
