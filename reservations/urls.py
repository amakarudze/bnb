from django.urls import path

from . import views
from .views import edit_reservation

app_name = "reservations"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("reservations_list", views.reservations_list, name="reservations_list"),
    path(
        "update_reservation/<uuid:pk>/",
        views.UpdateReservationView.as_view(),
        name="update_reservation",
    ),
    path("add_reservation/", views.add_reservation, name="add_reservation"),
    path("reports/", views.reports, name="reports"),
    path("search_reports/", views.search_reports, name="search_reports"),
    path("edit_reservation/<uuid:pk>/", views.edit_reservation, name="edit_reservation")
]
