from collections import Counter
from datetime import datetime

from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import UpdateView
from django.urls import reverse

from accounts.views import FROM_EMAIL, send_email
from events.models import Event
from rooms.models import Room
from website.forms import SearchForm


from .forms import (
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


@login_required
@permission_required(
    ["reservations.add_reservation", "accounts.add_user", "accounts.add_userprofile"],
    raise_exception=True,
)
def add_reservation(request):
    if request.method == "POST":
        form = NewReservationForm(request.POST)
        print(form.errors)
        user_id = request.POST.get("user")
        print(user_id)

        if form.is_valid():
            reservation = form.save()
            reservation.save()
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

    check_in_date = (
        ""
        if request.session["check_in_date"] is None
        else request.session["check_in_date"]
    )
    check_out_date = (
        ""
        if request.session["check_out_date"] is None
        else request.session["check_out_date"]
    )
    rooms = request.session["rooms"]
    events = request.session["events"]

    event_ids = list()
    if events is not None:
        for object in serializers.deserialize("json", events):
            pk = object.object.pk
            event_ids.append(pk)

    room_ids = list()
    if rooms is not None:
        for object in serializers.deserialize("json", rooms):
            pk = object.object.pk
            room_ids.append(pk)

    form = NewReservationForm(
        initial={
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "number_of_adults": ""
            if request.session["number_of_adults"] is None
            else request.session["number_of_adults"],
            "number_of_children": ""
            if request.session["number_of_children"] is None
            else request.session["number_of_children"],
        }
    )
    available_rooms = Room.objects.filter(id__in=room_ids)
    upcoming_events = Event.objects.filter(id__in=event_ids)
    form.fields["rooms"].queryset = available_rooms
    form.fields["events"].queryset = upcoming_events
    check_in = datetime.strptime(check_in_date, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out_date, "%Y-%m-%d").date()
    number_of_nights = (check_out - check_in).days
    available_rooms = available_rooms.annotate(
        total_price=F("price") * number_of_nights
    )

    return render(
        request,
        "reservations/reservation.html",
        {
            "form": form,
            "title": "Add Reservation",
            "available_rooms": available_rooms,
            "upcoming_events": upcoming_events,
            "number_of_nights": number_of_nights,
        },
    )


@login_required
def reports(request):
    if not request.user.is_superuser:
        return redirect("website:home")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    start_day = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_day = datetime.strptime(end_date, "%Y-%m-%d").date()
    difference = end_day - start_day
    period = difference.days
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
    total_rooms = Room.objects.all()
    booked_rooms = []
    for reservation in reservations:
        for room in reservation.rooms.all():
            booked_rooms.append(room.room_type)
    counters = Counter(booked_rooms)
    result_dict = dict(counters)
    result = result_dict
    result = {key: round((value / period) * 100, 2) for key, value in result.items()}

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
            "result": result,
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


class UpdateReservationView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = "reservations/reservation_update.html"
    permission_required = "reservations.change_reservation"
    raise_exception = True

    def get_success_url(self) -> str:
        reservation = self.get_object()
        if reservation.is_cancelled:
            message = render_to_string(
                "emails/guest_cancellation_confirmation.html",
                {
                    "name": reservation.user.first_name,
                    "username": reservation.user.email,
                },
            )
            from_email = FROM_EMAIL
            to_email = [reservation.user.email]
            subject = "Your reservation is cancelled!"
            send_email(subject, message, from_email, to_email)
            messages.success(self.request, "Reservation is successfully cancelled.")
        return reverse("reservations:reservations_list")
