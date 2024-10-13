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
            }
        )
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id": "check_out_date",
                "class": "form-control mr-sm-2",
                "placeholder": "YYYY-MM-DD",
            }
        )
    )
    number_of_adults = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "id": "number_of_adults",
                "class": "form-control mr-sm-2",
                "placeholder": "Number of adults",
            }
        )
    )
    number_of_children = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "id": "number_of_children",
                "class": "form-control mr-sm-2",
                "placeholder": "Number of children",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")
        number_of_adults = self.cleaned_data.get("number_of_adults")

        if check_in_date < date.today() or check_out_date < date.today():
            raise ValidationError(
                "Check in date or check out date cannot be in the past."
            )
        if check_in_date >= check_out_date:
            raise ValidationError(
                "Check out date should be greater than check in date."
            )

        if number_of_adults == 0:
            raise ValidationError("Number of adult guests cannot be 0.")
