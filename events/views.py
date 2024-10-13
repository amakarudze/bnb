from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse


from .forms import EventForm
from .models import Event


@login_required
@permission_required("events.add_event", raise_exception=True)
def add_event(request):
    form = EventForm()

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("events:events_list")
    return render(request, "events/event.html", {"title": "Add Event", "form": form})


@login_required
@permission_required("events.view_event", raise_exception=True)
def events_list(request):
    events = Event.objects.all()
    return render(
        request, "events/events_list.html", {"title": "View Events", "events": events}
    )


class UpdateEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event.html"
    permission_required = "events.change_event"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse("events:events_list")
