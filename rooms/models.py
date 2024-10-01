import uuid

from django.db import models

ROOM_TYPES = [
    ("Single", "Single"),
    ("Double/Twin", "Double/Twin"),
    ("Family", "Family"),
]
BATHROOM_TYPES = [
    ("Ensuite", "Ensuite"),
    ("Shared", "Shared"),
]


class Room(models.Model):
    """Model for storing room details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField()
    bed_type = models.CharField(max_length=10)
    number_of_beds = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    bathroom = models.CharField(max_length=20, choices=BATHROOM_TYPES)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.name
