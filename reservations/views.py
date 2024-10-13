from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse

from .models import Reservation
from .forms import ReservationsUpdateForm, GuestFormSet


@login_required
def dashboard(request):
    """Dashboard page for the staff reservation website"""
    return render(request, "reservations/index.html", {"title": "Home"})


@login_required
@permission_required("reservations.view_reservation", raise_exception=True)
def reservations_list(request):
    reservations = (
        Reservation.objects.prefetch_related("guest_set")
        .all()
        .order_by("-check_in_date")
    )
    return render(
        request,
        "reservations/reservations_list.html",
        {"title": "Reservations List", "reservations": reservations},
    )


class UpdateReservationsView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationsUpdateForm
    template_name = "website/reservation.html"
    permission_required = "reservations.change_reservations"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse("reservations:reservations_list")

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Reservation"
        context["guest_formset"] = GuestFormSet()
        return context
