import uuid

from django.db import models

ROOM_TYPES = [
    ("Single", "Single"),
    ("Double/Twin", "Double/Twin"),
    ("Family", "Family"),
    ("Queen", "Queen"),
    ("Executive", "Executive"),
    ("Honeymoon Suite", "Honeymoon Suite"),
]
BATHROOM_TYPES = [
    ("Ensuite", "Ensuite"),
    ("Shared", "Shared"),
]

BED_TYPES = [
    ("Single", "Single"),
    ("Three Quater", "Three Quarter"),
    ("Double", "Double"),
    ("Queen", "Queen"),
    ("King", "King"),
]


class Room(models.Model):
    """Model for storing room details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to="images")
    bed_type = models.CharField(max_length=15, choices=BED_TYPES)
    number_of_beds = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    bathroom = models.CharField(max_length=20, choices=BATHROOM_TYPES)
    room_capacity = models.IntegerField(default=2)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.name
