from django.db.models import Q
from django.shortcuts import render

from reservations.models import Reservation
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


def about_us(request):
    message = {
        "message": "We are a Bed and Breakfast place located in Karlskrona, Sweden. We started our small business in Autumn 2024. We welcome guests from all over the world to come and relax in our cozy rooms and enjoy the view of the Baltic Sea.",
    }
    return render(request, "website/about_us.html", message)


def contact_us(request):
    message = {
        "message": "Feel free to reach our Desk for support: +46 7779815118. We are available Monday to Sunday 9.00 to 12.00 to answer your queries! Wish you all the best! ",
    }
    return render(request, "website/contact_us.html", message)
