from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("make_reservation/", views.make_reservation, name="make_reservation"),
    path("reservation_success/", views.reservation_success, name="reservation_success"),
]
