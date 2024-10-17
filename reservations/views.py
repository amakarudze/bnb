from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView


from .forms import GuestFormSet, StaffReservationForm, ReservationUpdateForm
from .models import Reservation


@login_required
def dashboard(request):
    """Dashboard page for the staff reservation website"""
    if not request.user.is_staff:
        messages.error(request, "You need to be staff to access this page")
        return redirect("website:home")
    return render(request, "reservations/index.html", {"title": "Dashboard"})


@login_required
@permission_required("reservations.view_reservation", raise_exception=True)
def reservations_list(request):
    if not request.user.is_staff:
        messages.error(request, "You need to be staff to access this page")
        return redirect("website:home")
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


class UpdateReservationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = "website/reservation.html"
    permission_required = "reservations.change_reservation"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse("reservations:reservations_list")

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Reservation"
        context["guest_formset"] = GuestFormSet()
        return context


@login_required
@permission_required(
    ["reservations.add_reservations", "accounts.add_user"], raise_exception=True
)
def add_reservation(request):
    form = StaffReservationForm()
    return render(request, "reservations/reservation.html", {"form": form})


@login_required
def reports(request):
    if not request.user.is_superuser:
        return redirect("website:home")
    return render(request, "reservations/reports.html", {"title": "Reports"})
