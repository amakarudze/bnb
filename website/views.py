from django.db.models import Q
from django.shortcuts import render, redirect

from resetvations.forms import ReservationForm, GuestFormSet
from reservations.models import Guest, Reservation
from rooms.models import Room


def home(request):
    check_in = request.GET.get("check_in_date")
    check_out = request.GET.get("check_out_date")
    print(check_in, check_out)

    check_in_date = request.GET.get("check_in_date")
    check_out_date = request.GET.get("check_out_date")
    # number_of_adults = request.GET.get("number_of_adults")
    # number_of_children = request.POST.get("number_of_children")

    if check_in and check_out:
        try:
            booked_rooms = Reservation.objects.filter(
                Q(check_in_date__lte=check_in_date, check_out_date__gt=check_out_date)
                | Q(check_in_date__gte=check_in_date, check_out_date__lt=check_out_date)
                | Q(
                    check_in_date__lte=check_in_date, check_out_date__lte=check_out_date
                )
            ).only("rooms")
            print(booked_rooms)
            available_rooms = Room.objects.exclude(pk__in=booked_rooms)
        except Reservation.DoesNotExist:
            pass
    else:
        available_rooms = Room.objects.all()

    return render(
        request,
        "website/index.html",
        {"title": "Home", "available_rooms": available_rooms},
    )


def make_reservation(request):
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        guest_formset = GuestFormSet(request.POST)

        if reservation_form.is_valid() and guest_formset.is_valid():
            # Save the reservation
            reservation = reservation_form.save(commit=False)
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
        reservation_form = ReservationForm()
        guest_formset = GuestFormSet(
            queryset=Guest.objects.all()
        )  # Empty formset for guests

    return render(
        request,
        "website/reservation.html",
        {
            "reservation_form": reservation_form,
            "guest_formset": guest_formset,
        },
    )


def reservation_success(request):
    return render(request, "website/reservation_success.html")

  
  
    check_in = request.GET.get("check_in_date")
    check_out = request.GET.get("check_out_date")
    print(check_in, check_out)

    check_in_date = request.GET.get("check_in_date")
    check_out_date = request.GET.get("check_out_date")
    # number_of_adults = request.GET.get("number_of_adults")
    # number_of_children = request.POST.get("number_of_children")

    if check_in and check_out:
        try:
            booked_rooms = Reservation.objects.filter(
                Q(check_in_date__lte=check_in_date, check_out_date__gt=check_out_date)
                | Q(check_in_date__gte=check_in_date, check_out_date__lt=check_out_date)
                | Q(
                    check_in_date__lte=check_in_date, check_out_date__lte=check_out_date
                )
            ).only("rooms")
            print(booked_rooms)
            available_rooms = Room.objects.exclude(pk__in=booked_rooms)
        except Reservation.DoesNotExist:
            pass
    else:
        available_rooms = Room.objects.all()

    return render(
        request,
        "website/index.html",
        {"title": "Home", "available_rooms": available_rooms},
    )


def about_us(request):
    return render(request, "website/about_us.html")


def contact_us(request):
    return render(request, "website/contact_us.html")
