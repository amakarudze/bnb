from collections import Counter
from datetime import datetime

from django.db import IntegrityError
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView

from accounts.models import User, UserProfile
from accounts.views import FROM_EMAIL, send_email
from events.models import Event
from rooms.models import Room
from website.forms import SearchForm

from .forms import (
    AddReservationForm,
    NewReservationForm,
    ReservationUpdateForm,
    SearchReportsForm,
)
from .models import Reservation


@login_required
def dashboard(request):
    """Dashboard page for the staff reservation website"""
    form = SearchForm()
    if not request.user.is_staff:
        messages.error(request, "You need to be staff to access this page")
        return redirect("website:home")
    return render(
        request, "reservations/dashboard.html", {"title": "Dashboard", "form": form}
    )


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
    template_name = "reservations/reservation_update.html"
    permission_required = "reservations.change_reservation"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse("reservations:reservations_list")

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Reservation"
        return context


@login_required
@permission_required(
    ["reservations.add_reservations", "accounts.add_user"], raise_exception=True
)
def add_reservation(request):
    if request.method == "POST":
        form = AddReservationForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.create_user(
                    email=form.cleaned_data.get("email"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    password=form.cleaned_data.get("password"),
                )
                UserProfile.objects.create(
                    user=user,
                    dob=form.cleaned_data.get("dob"),
                    address=form.cleaned_data.get("address"),
                    city=form.cleaned_data.get("city"),
                    postal_code=form.cleaned_data.get("postal_code"),
                    state=form.cleaned_data.get("state"),
                    country=form.cleaned_data.get("country"),
                    phone_number=form.cleaned_data.get("phone_number"),
                )
                reservation = Reservation.objects.create(
                    user=user,
                    number_of_adults=form.cleaned_data.get("number_of_adults"),
                    number_of_children=form.cleaned_data.get("number_of_children"),
                    check_in_date=form.cleaned_data.get("check_in_date"),
                    check_out_date=form.cleaned_data.get("check_out_date"),
                )
                rooms = form.cleaned_data.get("rooms")
                for room in rooms:
                    reservation.rooms.set(room)
                events = form.cleaned_data.get("event")
                if events:
                    for event in events:
                        reservation.events.set(event)

                message = render_to_string(
                    "emails/guest_reservation_confirmation.html",
                    {
                        "name": reservation.user.first_name,
                        "booking_code": reservation.booking_code,
                        "check_in_date": reservation.check_in_date,
                        "check_out_date": reservation.check_out_date,
                        "rooms": reservation.rooms.all(),
                    },
                )

                subject = "Your booking confirmation at BnB!"
                from_email = FROM_EMAIL
                send_email(subject, message, from_email, [reservation.user.email])

                messages.success(request, "New reservation added successfully")
                return redirect("reservations:reservations_list")
            except IntegrityError:
                messages.error(request, "User with that email already exist")
                return redirect("reservations:new_reservation")
    else:
        check_in_date = request.session["check_in_date"]
        check_out_date = request.session["check_out_date"]
        event_ids = list()
        for object in serializers.deserialize("json", request.session["events"]):
            pk = object.object.pk
            event_ids.append(pk)

        room_ids = list()
        for object in serializers.deserialize("json", request.session["rooms"]):
            pk = object.object.pk
            room_ids.append(pk)
        form = AddReservationForm(
            initial={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "number_of_adults": request.session["number_of_adults"],
                "number_of_children": request.session["number_of_children"],
            }
        )
        form.fields["rooms"].queryset = Room.objects.filter(id__in=room_ids)
        form.fields["events"].queryset = Event.objects.filter(id__in=event_ids)

    return render(
        request,
        "reservations/reservation.html",
        {"form": form, "title": "Add Reservation"},
    )


@login_required
def reports(request):
    if not request.user.is_superuser:
        return redirect("website:home")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    reservations = Reservation.objects.filter(
        check_in_date__gte=start_date, check_in_date__lte=end_date
    ).prefetch_related("rooms")
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
    rooms = reservations.only("rooms")
    booked_rooms = list()

    for reservation in reservations:
        for room in reservation.rooms.all():
            booked_rooms.append(room.pk)

    counter_rooms = Counter(booked_rooms)
    report_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    report_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    period = (report_end_date - report_start_date).days

    total_reservations = reservations.count()
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
            "start_date": start_date,
            "end_date": end_date,
            "total_rooms": total_rooms,
            "reservations": total_reservations,
            "room_occupancy": rooms,
            "counter_rooms": counter_rooms,
            "period": period,
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
def new_reservation(request):
    if request.method == "POST":
        form = NewReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            message = render_to_string(
                "emails/guest_reservation_confirmation.html",
                {
                    "name": reservation.user.first_name,
                    "booking_code": reservation.booking_code,
                    "check_in_date": reservation.check_in_date,
                    "check_out_date": reservation.check_out_date,
                    "rooms": reservation.rooms.all(),
                },
            )

            subject = "Your booking confirmation at BnB!"
            from_email = FROM_EMAIL
            send_email(subject, message, from_email, [reservation.user.email])

            messages.success(request, "New reservation added successfully")
            return redirect("reservations:reservations_list")
    else:
        check_in_date = request.session["check_in_date"]
        check_out_date = request.session["check_out_date"]
        event_ids = list()

        for object in serializers.deserialize("json", request.session["events"]):
            pk = object.object.pk
            event_ids.append(pk)
        room_ids = list()
        for object in serializers.deserialize("json", request.session["rooms"]):
            pk = object.object.pk
            room_ids.append(pk)
        form = NewReservationForm(
            initial={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "number_of_adults": request.session["number_of_adults"],
                "number_of_children": request.session["number_of_children"],
            }
        )
        form.fields["rooms"].queryset = Room.objects.filter(id__in=room_ids)
        form.fields["events"].queryset = Event.objects.filter(id__in=event_ids)
    return render(
        request,
        "reservations/new_reservation.html",
        {"title": "Add New Reservation", "form": form},
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

            return redirect("reservations:reservation_list")

    else:
        form = ReservationUpdateForm(instance=reservation)

    return render(
        request,
        "reservations/update_reservation.html",
        {"form": form, "title": "Update Reservation", "reservation": reservation},
    )
