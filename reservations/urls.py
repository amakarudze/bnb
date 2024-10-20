from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reservations_list/", views.reservations_list, name="reservations_list"),
    path(
        "edit_reservation/<uuid:pk>/",
        views.edit_reservation,
        name="edit_reservation",
    ),
    path("add_reservation/", views.add_reservation, name="add_reservation"),
    path("reports/", views.reports, name="reports"),
    path("search_reports/", views.search_reports, name="search_reports"),
]
