from django import forms

from .models import BATHROOM_TYPES, BED_TYPES, ROOM_TYPES, Room


class RoomForm(forms.ModelForm):
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
    bed_type = forms.ChoiceField(
        choices=BED_TYPES,
        widget=forms.Select(attrs={"class": "form-control", "id": "bed_type"}),
    )
    room_type = forms.ChoiceField(
        choices=ROOM_TYPES,
        widget=forms.Select(attrs={"class": "form-control", "id": "room_type"}),
    )
    bathroom = forms.ChoiceField(
        choices=BATHROOM_TYPES,
        widget=forms.Select(attrs={"class": "form-control", "id": "bathroom"}),
    )
    photo = forms.ImageField()

    class Meta:
        model = Room
        fields = [
            "name",
            "description",
            "photo",
            "bed_type",
            "number_of_beds",
            "room_type",
            "bathroom",
            "room_capacity",
            "price",
        ]
