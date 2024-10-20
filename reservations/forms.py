from datetime import date
from django import forms

from accounts.forms import SignUpForm
from events.models import Event

from .models import Reservation, Guest


class ReservationForm(forms.ModelForm):
    """
    Form for creating a reservation.
    """

    check_in_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "DD/MM/YYYY",
                "type": "date",
            }
        )
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "DD/MM/YYYY",
                "type": "date",
            }
        )
    )
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Reservation
        fields = [
            "number_of_adults",
            "number_of_children",
            "rooms",
            "events",
            "check_in_date",
            "check_out_date",
        ]
        widgets = {
            "rooms": forms.CheckboxSelectMultiple,
            "number_of_adults": forms.TextInput(attrs={"class": "form-control"}),
            "number_of_children": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        check_in_date = self.cleaned_data.get("check_in_date")
        check_out_date = self.cleaned_data.get("check_out_date")

        if check_out_date and check_in_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError(
                    {
                        "check_out_date": [
                            "Check-out date must be after the check-in date."
                        ]
                    }
                )
            if check_in_date < date.today():
                raise forms.ValidationError(
                    {"check_in_date": ["Check-in date should not be a past date."]}
                )


class GuestForm(forms.ModelForm):
    """
    Form for collecting guest details.
    """

    class Meta:
        model = Guest
        fields = ["full_name", "is_adult"]


GuestFormSet = forms.modelformset_factory(
    Guest,
    form=GuestForm,
    extra=1,
    can_delete=True,
)


class ReservationUpdateForm(ReservationForm):
    is_paid = forms.BooleanField(required=False)
    checked_in = forms.BooleanField(required=False)
    checked_out = forms.BooleanField(required=False)
    is_cancelled = forms.BooleanField(required=False)


class AddReservationForm(ReservationForm, SignUpForm):
    pass


class SearchReportsForm(forms.Form):
    start_date = forms.DateField(
        label="Enter Start Date:",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "id": "start_date",
                "placeholder": "DD/MM/YYYY",
                "type": "date",
            }
        ),
    )
    end_date = forms.DateField(
        label="Enter End Date:",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "id": "end_date",
                "placeholder": "DD/MM/YYYY",
                "type": "date",
            }
        ),
    )

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    {"end_date": ["End  date must be greater than Start date."]}
                )

            if end_date > date.today():
                raise forms.ValidationError(
                    {"end_date": ["End date should not be a future date."]}
                )
            if start_date > date.today():
                raise forms.ValidationError(
                    {"start_date": ["Start date should not be a future date."]}
                )


class EditReservationForm(forms.ModelForm):
    # Guest update form
    is_cancelled = forms.BooleanField(required=False)

    class Meta:
        model = Reservation
        fields = ["number_of_adults", "number_of_children", "events", "is_cancelled"]
        widgets = {
            "events": forms.CheckboxSelectMultiple,
            "number_of_adults": forms.NumberInput(attrs={"class": "form-control"}),
            "number_of_children": forms.NumberInput(attrs={"class": "form-control"}),
        }
