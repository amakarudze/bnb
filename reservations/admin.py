from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .forms import NewReservationForm
from .models import Guest, Reservation


class ReservationsModelAdmin(ModelAdmin):
    form = NewReservationForm()
    filter_horizontal = ("user",)


admin.site.register(Guest)
admin.site.register(Reservation)
