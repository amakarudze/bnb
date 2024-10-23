from django import forms

from .models import AGE_RESTRICTIONS, Event


class EventForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Enter Event Name",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "description",
                "placeholde": "Describe the event for guests.",
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
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id": "start_date",
                "class": "form-control mr-sm-2",
                "placeholder": "YYYY-MM-DD",
                "type": "date",
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "id": "end_date",
                "class": "form-control mr-sm-2",
                "placeholder": "YYYY-MM-DD",
                "type": "date",
            }
        )
    )
    min_participants = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "min_participants",
                "class": "form-control mr-sm-2",
                "placeholder": 0,
            }
        )
    )
    max_participants = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "max_participants",
                "class": "form-control mr-sm-2",
                "placeholder": 0,
            }
        )
    )
    num_participants = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "num_participants",
                "class": "form-control mr-sm-2",
                "placeholder": 0,
            }
        )
    )
    fully_booked = forms.BooleanField(
        required=False,
    )
    price = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "id": "price",
                "class": "form-control mr-sm-2",
                "placeholder": 0,
            }
        )
    )

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
