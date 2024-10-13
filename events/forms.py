from django import forms

from .models import AGE_RESTRICTIONS, Event


class EventForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Enter Room Name",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "description",
                "placeholde": "Describe the room for guests.",
            }
        )
    )
    photo = forms.ImageField(required=False)
    host = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "host",
                "placeholder": "Enter Event Host",
            }
        )
    )
    venue = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "venue",
                "placeholde": "Enter Venue Details",
            }
        )
    )
    start_date = forms.DateField()
    end_date = forms.DateField()
    min_participants = forms.IntegerField()
    max_participants = forms.IntegerField()
    num_participants = forms.IntegerField()
    fully_booked = forms.BooleanField(
        required=False,
    )
    price = forms.FloatField()

    age_restrictions = forms.ChoiceField(
        choices=AGE_RESTRICTIONS,
        widget=forms.Select(attrs={"class": "form-control", "id": "age_restrictions"}),
    )

    additional_information = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "additional_information",
                "placeholde": "Enter Additional Information",
            }
        ),
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "photo",
            "host",
            "venue",
            "start_date",
            "end_date",
            "min_participants",
            "max_participants",
            "num_participants",
            "fully_booked",
            "price",
            "age_restrictions",
            "additional_information",
        ]
