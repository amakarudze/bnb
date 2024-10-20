from datetime import date, datetime
from django import forms

from accounts.forms import SignUpForm
from events.models import Event
from rooms.models import Room

from accounts.models import User

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
    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.filter(can_be_rented=True),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
    )
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.filter(start_date__gte=datetime.now()),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
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
            "number_of_adults": forms.NumberInput(attrs={"class": "form-control"}),
            "number_of_children": forms.NumberInput(attrs={"class": "form-control"}),
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

    full_name = forms.CharField(
        label="Full name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Full name"}
        ),
    )
    is_adult = forms.BooleanField(
        label="Is Adult",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "type": "checkbox",
                "value": "",
                "required": False,
            }
        ),
    )


GuestFormSet = forms.formset_factory(GuestForm, extra=1, max_num=10, validate_min=True)


class ReservationUpdateForm(ReservationForm):
    is_paid = forms.BooleanField(required=False)
    checked_in = forms.BooleanField(required=False)
    checked_out = forms.BooleanField(required=False)
    is_cancelled = forms.BooleanField(required=False)


class AddReservationForm(ReservationForm, SignUpForm):
    pass


class NewReservationForm(ReservationForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


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
