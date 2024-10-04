from django import forms
from .models import Reservation, Guest
from rooms.models import Room
from events.models import Event

class ReservationForm(forms.ModelForm):
    """
    Form for creating a reservation.
    """

    class Meta:
        model = Reservation
        fields = [
            'number_of_adults',
            'number_of_children',
            'rooms',
            'events',
            'check_in_date',
            'check_out_date',
        ]
        widgets = {
            'rooms': forms.CheckboxSelectMultiple,  # Assuming multiple rooms can be selected
            'events': forms.CheckboxSelectMultiple,  # Assuming multiple events can be selected
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_out_date and check_in_date and check_out_date <= check_in_date:
            raise forms.ValidationError("Check-out date must be after the check-in date.")

        return cleaned_data


class GuestForm(forms.ModelForm):
    """
    Form for collecting guest details.
    """

    class Meta:
        model = Guest
        fields = ['full_name', 'is_adult']

# Creating a formset to handle multiple guests
GuestFormSet = forms.modelformset_factory(
    Guest, 
    form=GuestForm, 
    extra=1,  # The initial number of empty forms displayed
    can_delete=True  # Allow deleting guests from the formset
)
