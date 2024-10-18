from datetime import date
from django import forms

from events.models import Event

from .models import Reservation, Guest

from accounts.forms import SignUpForm

class ReservationForm(forms.ModelForm):
    """
    Form for creating a reservation.
    """

    check_in_date = forms.DateField()
    check_out_date = forms.DateField()
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
                    "Check-out date must be after the check-in date."
                )
            if check_in_date < date.today():
                raise forms.ValidationError("Check-in date should not be a past date.")


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


class ReservationsUpdateForm(ReservationForm):
    is_paid = forms.BooleanField(required=False)
    checked_in = forms.BooleanField(required=False)
    checked_out = forms.BooleanField(required=False)
    

class AddReservationForm(ReservationForm, SignUpForm):
    pass

