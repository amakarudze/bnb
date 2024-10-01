import uuid

from django.db import models

AGE_RESTRICTIONS = [
    ("None", "None"),
    ("Below 12 years", "Below 12 years"),
    ("12 years+", "12 years+"),
    ("18 years+", "18 years+"),
    ("21 years+", "21 years+"),
    ("50 yeards+", "50 years+"),
    ("60 years+", "60 years+"),
]


class Event(models.Mode):
    """Model for storing event details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField()
    host = models.CharField()
    venue = models.CharField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    min_participants = models.IntegerField()
    max_participants = models.IntegerField()
    num_participants = models.IntegerField()
    fully_booked = models.BooleanField(default=False)
    price = models.FloatField()
    age_restrictions = models.CharField(max_length=20, choices=AGE_RESTRICTIONS)
    additional_information = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.name
