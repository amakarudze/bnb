from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from events.models import Event
from reservations.forms import ReservationForm, GuestFormSet
from reservations.models import Guest, Reservation
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
            # Save the reservation
            reservation = form.save(commit=False)
            reservation.user = request.user  # Set the current logged-in user
            reservation.save()

            # Save guests associated with the reservation
            for guest_form in guest_formset:
                if guest_form.cleaned_data:  # Ensure the form is filled
                    guest = guest_form.save(commit=False)
                    guest.reservation = reservation
                    guest.save()

            return redirect("website:reservation_success")  # Redirect to a success page

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


def reservation_success(request):
    return render(request, "website/reservation_success.html")


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


def cancel_reservation(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id)

    # Get the associated reservation
    reservation = guest.reservation

    if reservation.is_cancelled:
        return HttpResponse("This reservation is already canceled.")

    # Mark the reservation as canceled
    reservation.is_cancelled = True
    reservation.save()