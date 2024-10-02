from django.contrib import admin

from .models import Guest, Reservation

admin.site.register(Guest)
admin.site.register(Reservation)
