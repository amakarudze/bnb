from django.urls import path

from . import views

app_name = "rooms"

urlpatterns = [
    path("add_room/", views.add_room, name="add_room"),
    path("update/room/<uuid:pk>/", views.UpdateRoomView.as_view(), name="update_room"),
    path("rooms_list/", views.rooms_list, name="rooms_list"),
]
