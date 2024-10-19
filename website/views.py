from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from events.models import Event
from reservations.forms import ReservationForm, EditReservationForm
from reservations.models import Reservation
from website.forms import SearchByBookingCodeForm
from rooms.models import Room

from .forms import SearchForm


def home(request):
    available_rooms = Room.objects.filter(can_be_rented=True)[:6]
    form = SearchForm()
    return render(
        request,
        "website/index.html",
        {"title": "Home", "available_rooms": available_rooms, "form": form},
    )


@login_required
def make_reservation(request, pk):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        guest_formset = GuestFormSet(request.POST)

        if form.is_valid() and guest_formset.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.calculate_total_cost()
            reservation.save()

            for guest_form in guest_formset:
                if guest_form.cleaned_data:
                    guest = guest_form.save(commit=False)
                    guest.reservation = reservation
                    guest.save()

            return redirect("website:reservation_success")

    else:
        room = Room.objects.get(pk=pk)
        check_in_date = request.GET.get("check_in_date")
        check_out_date = request.GET.get("check_out_date")
        if check_in_date and check_out_date:
            events = Event.objects.filter(
                start_date__gte=check_in_date, end_date__lte=check_out_date
            )
            if events:
                form = ReservationForm(
                    initial={
                        "rooms": room,
                        "events": events,
                        "check_in_date": check_in_date,
                        "check_out_date": check_out_date,
                    }
                )
        else:
            form = ReservationForm(initial={"rooms": room})
        guest_formset = GuestFormSet(queryset=Guest.objects.all())

    return render(
        request,
        "website/reservation.html",
        {
            "form": form,
            "guest_formset": guest_formset,
        },
    )


@login_required
def reservation_success(request):
    return render(
        request,
        "website/reservation_success.html",
        {"title": "Rerservation successful!"},
    )


def search(request):
    check_in_date = request.GET.get("check_in_date", "")
    check_out_date = request.GET.get("check_out_date", "")
    number_of_adults = request.GET.get("number_of_adults", "")
    number_of_children = request.GET.get("number_of_children", "")
    print(number_of_children)

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
        pass

    return render(
        request,
        "website/search_results.html",
        {"title": "Search for rooms", "rooms": rooms},
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

      
def search_by_booking_code(request):
    form = SearchByBookingCodeForm()
    return render(
        request,
        "website/search_by_booking_code.html",
        {"title": "Search By Booking Code", "form": form},
    )


def search_result_by_booking_code(request):
    booking_code = request.GET.get("booking_code")
    reservation_detail = Reservation.objects.filter(booking_code=booking_code)
    return render(
        request,
        "website/search_result_by_booking_code.html",
        {"title": "Search Result By Booking Code", "reservations": reservation_detail},
    )


@login_required
def update_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save()
            if updated_reservation.is_cancelled == True:
                message = render_to_string(
                    "emails/guest_cancellation_confirmation.html",
                    {"name": user.first_name, "username": user.email},
                )
                from_email = FROM_EMAIL
                to_email = [reservation.user.email]
                subject = "Your reservation is cancelled!"
                send_email(subject, message, from_email, to_email)

                messages.success(request, "Reservation updated successfully!")   

            return redirect('website:reservations')    

    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'website/update_reservation.html', {'form': form, 'title':'Update Reservation', "reservation": reservation})