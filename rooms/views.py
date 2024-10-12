from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse


from .forms import RoomForm
from .models import Room


@login_required
@permission_required("rooms.add_room", raise_exception=True)
def add_room(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("rooms:rooms_list")
    return render(request, "rooms/room.html", {"title": "Add Room", "form": form})


@login_required
@permission_required("rooms.view_room", raise_exception=True)
def rooms_list(request):
    rooms = Room.objects.all()
    return render(
        request, "rooms/rooms_list.html", {"title": "View Rooms", "rooms": rooms}
    )


class UpdateRoomView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room.html"

    def get_success_url(self) -> str:
        return reverse("rooms:rooms_list")
