from datetime import date

from django import forms

from .models import Reservation, Guest
from events.models import Event
from accounts.forms import SignUpForm


class ReservationForm(forms.ModelForm):
    """
    Form for creating a reservation.
    """

    check_in_date = forms.DateField()
    check_out_date = forms.DateField()

    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        label="Events",
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control",
                "id": "events",
            }
        ),
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
            # 'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            # 'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        check_in_date = self.cleaned_data.get("check_in_date")
        check_out_date = self.cleaned_data.get("check_out_date")

        if check_out_date and check_in_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError(
                    "Check-out date must be after the check-in date."
                )
            if check_in_date < date.today():
                raise forms.ValidationError("Check-in date should not be a past date.")

        # return check_in_date, check_out_date


class GuestForm(forms.ModelForm):
    """
    Form for collecting guest details.
    """

    class Meta:
        model = Guest
        fields = ["full_name", "is_adult"]


# Creating a formset to handle multiple guests
GuestFormSet = forms.modelformset_factory(
    Guest,
    form=GuestForm,
    extra=1,  # The initial number of empty forms displayed
    can_delete=True,  # Allow deleting guests from the formset
)


class StaffReservationForm(SignUpForm):
    pass