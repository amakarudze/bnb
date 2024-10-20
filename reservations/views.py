from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView

from accounts.views import FROM_EMAIL, send_email

from .forms import (
    GuestFormSet,
    AddReservationForm,
    ReservationUpdateForm,
    SearchReportsForm,
)
from .models import Reservation, Event, Room


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
    form = AddReservationForm()
    guest_formset = GuestFormSet()
    print(guest_formset)
    print(guest_formset.empty_form)
    return render(
        request,
        "reservations/reservation.html",
        {"form": form, "guest_formset": guest_formset},
    )


@login_required
def reports(request):
    if not request.user.is_superuser:
        return redirect("website:home")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    reservations = Reservation.objects.filter(
        check_in_date__gte=start_date, check_in_date__lte=end_date
    )
    events = Event.objects.filter(
        start_date__gte=start_date, start_date__lte=end_date
    ).count()
    total_revenue = reservations.aggregate(Sum("total_price"))["total_price__sum"]
    total_adults = reservations.aggregate(Sum("number_of_adults"))[
        "number_of_adults__sum"
    ]
    total_children = reservations.aggregate(Sum("number_of_children"))[
        "number_of_children__sum"
    ]
    total_bookings = reservations.filter(is_cancelled=False).count()
    total_rooms_booked = Reservation.rooms.through.objects.count()
    total_rooms = Room.objects.all()

    return render(
        request,
        "reservations/reports.html",
        {
            "title": "Reports",
            "total_revenue": total_revenue,
            "total_adults": total_adults,
            "total_children": total_children,
            "total_bookings": total_bookings,
            "events": events,
            "total_rooms_booked": total_rooms_booked,
            "start_date": start_date,
            "end_date": end_date,
            "total_rooms": total_rooms,
        },
    )


@login_required
def search_reports(request):
    if not request.user.is_superuser:
        return redirect("website:home")
    form = SearchReportsForm()
    return render(
        request,
        "reservations/search_reports.html",
        {"form": form, "Title": "Search reports"},
    )


@login_required
def edit_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)

    if request.method == "POST":
        form = ReservationUpdateForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save()
            if updated_reservation.is_cancelled:
                message = render_to_string(
                    "emails/guest_cancellation_confirmation.html",
                    {
                        "name": updated_reservation.user.first_name,
                        "username": updated_reservation.user.email,
                    },
                )
                from_email = FROM_EMAIL
                to_email = [reservation.user.email]
                subject = "Your reservation is cancelled!"
                send_email(subject, message, from_email, to_email)

                messages.success(request, "Reservation updated successfully!")

            return redirect("reservations:reservations_list")

    else:
        form = ReservationUpdateForm(instance=reservation)

    return render(
        request,
        "reservations/update_reservation.html",
        {"form": form, "title": "Update Reservation", "reservation": reservation},
    )
