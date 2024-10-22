from collections import Counter
from datetime import datetime

from django.db import IntegrityError
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from accounts.models import User, UserProfile
from accounts.views import FROM_EMAIL, send_email
from events.models import Event
from rooms.models import Room
from website.forms import SearchForm


from .forms import (
    AddReservationForm,
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
        form = AddReservationForm(request.POST)
        email = (request.POST.get("email"),)

        if form.is_valid():
            try:
                user = User.objects.create_user(
                    email=request.POST.get("email"),
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    password=request.POST.get("password"),
                )
                UserProfile.objects.create(
                    user=user,
                    dob=request.POST.get("dob"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    postal_code=request.POST.get("postal_code"),
                    state=request.POST.get("state"),
                    country=request.POST.get("country"),
                    phone_number=request.POST.get("phone_number"),
                )
            except IntegrityError:
                messages.error(request, "User with that email already exist")

                user = User.objects.get(email=email)
                reservation = Reservation.objects.create(
                    user=user,
                    number_of_adults=request.POST.get("number_of_adults"),
                    number_of_children=request.POST.get("number_of_children"),
                    check_in_date=request.POST.get("check_in_date"),
                    check_out_date=request.POST.get("check_out_date"),
                )
                rooms = request.POST.get("rooms")
                for room in rooms:
                    reservation.rooms.set(room)
                events = request.POST.get("events")
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

    check_in_date = request.session["check_in_date"]
    check_out_date = request.session["check_out_date"]
    rooms = request.session["rooms"]
    events = request.session["events"]

    event_ids = list()
    for object in serializers.deserialize("json", events):
        pk = object.object.pk
        event_ids.append(pk)

    room_ids = list()
    for object in serializers.deserialize("json", rooms):
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


@login_required
def edit_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)

    if request.method == "POST":
        form = ReservationUpdateForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            updated_reservation.save()
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
        "reservations/reservation_update.html",
        {"form": form, "title": "Update Reservation", "reservation": reservation},
    )
