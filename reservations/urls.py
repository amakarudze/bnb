from django.urls import path

from . import views
from .views import staff_sign_up_for_guest, make_reservation

app_name = "reservations"  # This defines the namespace

urlpatterns = [
    path('sign-up-for-guest/', views.staff_sign_up_for_guest, name='sign-up-for-guest'),
    path('make-reservation/', views.make_reservation, name='make-reservation'),
]
