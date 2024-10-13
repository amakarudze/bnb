from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("add_event/", views.add_event, name="add_event"),
    path(
        "update/event/<uuid:pk>/", views.UpdateEventView.as_view(), name="update_event"
    ),
    path("events_list/", views.events_list, name="events_list"),
]
