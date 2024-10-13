import uuid

from django.db import models

AGE_RESTRICTIONS = [
    ("No age restrictions", "No age restrictions"),
    ("Below 12 years", "Below 12 years"),
    ("12 years+", "12 years+"),
    ("18 years+", "18 years+"),
    ("21 years+", "21 years+"),
    ("50 yeards+", "50 years+"),
    ("60 years+", "60 years+"),
]


class Event(models.Model):
    """Model for storing event details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to="images", blank=True, null=True)
    host = models.CharField(max_length=100)
    venue = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    min_participants = models.IntegerField(default=0)
    max_participants = models.IntegerField(default=0)
    num_participants = models.IntegerField(default=0)
    fully_booked = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    age_restrictions = models.CharField(max_length=30, choices=AGE_RESTRICTIONS)
    additional_information = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.name
