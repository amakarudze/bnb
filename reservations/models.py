import uuid

from django.db import models

from accounts.models import User
from events.models import Event
from rooms.models import Room


class Reservation(models.Model):
    """Model for storing reservation details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_adults = models.IntegerField(default=0)
    number_of_children = models.IntegerField(default=0)
    rooms = models.ManyToManyField(Room, related_name="rooms_reserved")
    events = models.ManyToManyField(Event, related_name="events_reserved", blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_cost = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    booking_code = models.CharField(max_length=6)
    is_cancelled = models.BooleanField(default=False)


    class Meta:
        managed = True

    def __str__(self):
        return f"{self.user} {self.check_in_date} - {self.check_out_date}"

    def calculate_total_cost(self):
        total = 0
        self.total_cost = total
        self.save(update_fields=self.total_cost)


class Guest(models.Model):
    """Model for storing additional guests' details."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="guest_set"
    )
    full_name = models.CharField(max_length=100)
    is_adult = models.BooleanField(default=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.full_name
