from datetime import datetime

from django.db.models import F, Sum
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from accounts.models import User
from accounts.views import FROM_EMAIL, send_email
from events.models import Event
from reservations.forms import EditReservationForm, ReservationForm
from reservations.models import Reservation
from website.forms import SearchByBookingCodeForm
from rooms.models import Room

from .forms import SearchForm


def home(request):
    available_rooms = Room.objects.filter(can_be_rented=True)[:6]
    form = SearchForm()
    events = Event.objects.filter(fully_booked=False)
    return render(
        request,
        "website/index.html",
        {
            "title": "Home",
            "available_rooms": available_rooms,
            "form": form,
            "events": events,
        },
    )


@login_required
def make_reservation(request):
    form = ReservationForm(request.POST)
    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            reservation.save_m2m()

            subject = "Booking Confirmation - BNB"
            guest_email = reservation.user.email

            message = render_to_string(
                "emails/guest_reservation_confirmation.html",
                {
                    "reservation": reservation,
                    "booking_reference_code": reservation.booking_code,
                    "room_id": reservation.rooms.all(),
                    "check_in_date": reservation.check_in_date,
                    "check_out_date": reservation.check_out_date,
                },
            )

            send_email(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [guest_email],
            )

            guest_message = render_to_string(
                "emails/guest_reservation_confirmation.html",
                {
                    "name": reservation.user.first_name,
                    "booking_code": reservation.booking_code,
                    "check_in_date": reservation.check_in_date,
                    "check_out_date": reservation.check_out_date,
                    "rooms": reservation.rooms.all(),
                },
            )
            staff_message = render_to_string(
                "emails/staff_notifications.html",
                {
                    "booking_code": reservation.booking_code,
                    "check_in_date": reservation.check_in_date,
                    "check_out_date": reservation.check_out_date,
                    "rooms": reservation.rooms.all(),
                },
            )
            staff = [user.email for user in User.objects.filter(is_staff=True)]
            guest_subject = "Your booking confirmation at BnB!"
            staff_subject = "New booking notification!"
            from_email = FROM_EMAIL

            send_email(
                guest_subject, guest_message, from_email, [reservation.user.email]
            )
            send_email(staff_subject, staff_message, from_email, staff)

            messages.success(
                request, "Thank you for making a reservation to stay at the BnB!"
            )
            return redirect("website:reservations")

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

    event_ids = list()
    if request.session["events"]:
        for object in serializers.deserialize("json", request.session["events"]):
            pk = object.object.pk
            event_ids.append(pk)
    room_ids = list()
    if request.session["rooms"]:
        for object in serializers.deserialize("json", request.session["rooms"]):
            pk = object.object.pk
            room_ids.append(pk)
    form = ReservationForm(
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
        "website/reservation.html",
        {
            "form": form,
            "title": "Make Reservation",
            "upcoming_events": upcoming_events,
            "available_rooms": available_rooms,
        },
    )


def search(request):
    check_in_date = request.GET.get("check_in_date", "")
    check_out_date = request.GET.get("check_out_date", "")
    number_of_adults = request.GET.get("number_of_adults", "")
    number_of_children = request.GET.get("number_of_children", "")
    events = Event.objects.all()

    events = Event.objects.filter(
        start_date__date__lte=check_out_date, end_date__date__gte=check_in_date
    )
    reservations = Reservation.objects.filter(
        check_in_date__lte=check_out_date, check_out_date__gte=check_in_date
    )
    booked_rooms = []
    for reservation in reservations:
        for room in reservation.rooms.all():
            booked_rooms.append(room.pk)
    rooms = Room.objects.exclude(pk__in=booked_rooms)
    if int(number_of_children) > 0:
        suggested_rooms = rooms.filter(room_type="Family")
        if suggested_rooms:
            rooms = suggested_rooms
    else:
        rooms = rooms.exclude(room_type="Family")
    if number_of_adults:
        if (
            int(number_of_adults)
            > rooms.aggregate(Sum("room_capacity"))["room_capacity__sum"]
        ):
            messages.error(
                request,
                "We are sorry we don't have enough room to accommodate you all.",
            )
            rooms = None
    if rooms is not None:
        request.session["rooms"] = serializers.serialize("json", rooms)
    if events is not None:
        request.session["events"] = serializers.serialize("json", events)
    request.session["check_in_date"] = check_in_date
    request.session["check_out_date"] = check_out_date
    request.session["number_of_adults"] = number_of_adults
    request.session["number_of_children"] = number_of_children

    return render(
        request,
        "website/search_results.html",
        {"title": "Search for rooms", "rooms": rooms, "events": events},
    )


def about_us(request):
    return render(request, "website/about_us.html", {"title": "About us"})


def contact_us(request):
    return render(request, "website/contact_us.html", {"title": "Contact us"})


def rooms(request):
    rooms = Room.objects.filter(can_be_rented=True)
    return render(
        request, "website/search_results.html", {"rooms": rooms, "title": "Our Rooms"}
    )


def room(request, pk):
    room = Room.objects.get(pk=pk)
    return render(
        request, "website/room_details.html", {"title": "Room Details", "room": room}
    )


def event(request, pk):
    event = Event.objects.get(pk=pk)
    return render(
        request,
        "website/event_details.html",
        {"title": "Event Details", "event": event},
    )


@login_required
def reservations(request):
    reservation_list = Reservation.objects.filter(user=request.user).order_by(
        "-check_in_date"
    )
    return render(
        request,
        "website/reservations.html",
        {"title": "Manage Reservations", "reservation_list": reservation_list},
    )


@login_required
def update_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    form = EditReservationForm(instance=reservation)
    if request.method == "POST":
        if form.is_valid():
            is_cancelled = form.cleaned_data["is_cancelled"]
            if is_cancelled:
                guest_message = render_to_string(
                    "emails/guest_cancellation_confirmation.html",
                    {
                        "name": reservation.user.first_name,
                        "booking_code": reservation.booking_code,
                        "check_in_date": reservation.check_in_date,
                        "check_out_date": reservation.check_out_date,
                        "rooms": reservation.rooms.all(),
                    },
                )
            staff_message = render_to_string(
                "emails/staff_notifications_cancellations.html",
                {
                    "booking_code": reservation.booking_code,
                    "check_in_date": reservation.check_in_date,
                    "check_out_date": reservation.check_out_date,
                    "rooms": reservation.rooms.all(),
                },
            )
            staff = [user.email for user in User.objects.filter(is_staff=True)]
            guest_subject = "Your booking at BnB has been cancelled!"
            staff_subject = "New booking cancellation notification!"
            from_email = FROM_EMAIL

            send_email(
                guest_subject, guest_message, from_email, [reservation.user.email]
            )
            send_email(staff_subject, staff_message, from_email, staff)
    return render(
        request,
        "website/update_reservation.html",
        {"title": "Update reservation", "reservation": reservation},
    )


@login_required
def search_by_booking_code(request):
    form = SearchByBookingCodeForm()
    return render(
        request,
        "website/search_by_booking_code.html",
        {"title": "Search By Booking Code", "form": form},
    )


@login_required
def search_result_by_booking_code(request):
    booking_code = request.GET.get("booking_code")
    if request.user.is_staff:
        reservation_detail = Reservation.objects.filter(
            booking_code=booking_code
        ).first()
    else:
        reservation_detail = (
            Reservation.objects.filter(booking_code=booking_code)
            .filter(user=request.user)
            .first()
        )
    return render(
        request,
        "website/search_result_by_booking_code.html",
        {"title": "Search Result By Booking Code", "reservation": reservation_detail},
    )
