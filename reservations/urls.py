from django.urls import path
from .views import make_reservation_view

app_name = 'reservations'  # This defines the namespace

urlpatterns = [
    path('create_guest/', make_reservation_view, name='create_guest'),
]
