from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("reservations_list", views.reservations_list, name="reservations_list"),
    path(
        "update_reservation/<uuid:pk>/",
        views.UpdateReservationsView.as_view(),
        name="update_reservation",
    ),
]
