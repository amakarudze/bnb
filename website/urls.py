from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "make_reservation/<uuid:pk>/", views.make_reservation, name="make_reservation"
    ),
    path("reservation_success/", views.reservation_success, name="reservation_success"),
    path("about_us/", views.about_us, name="about_us"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("rooms/", views.rooms, name="rooms"),
    path("search/", views.search, name="search"),
    path("room/<uuid:pk>/", views.room, name="room"),
    path(
        "search_by_booking_code",
        views.search_by_booking_code,
        name="search_by_booking_code",
    ),
    path(
        "search_result_by_booking_code",
        views.search_result_by_booking_code,
        name="search_result_by_booking_code",
    ),
    path("cancel_reservation/<uuid:pk>", views.cancel_reservation, name="cancel_reservation")

]
