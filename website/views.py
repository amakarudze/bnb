from datetime import date

from django.db.models import Q
from django.shortcuts import render

from reservations.models import Reservation
from rooms.models import Room


def home(request):
    check_in = request.GET.get("check_in_date")
    check_out = request.GET.get("check_out_date")
    print(check_in, check_out)
    check_in_date = date(check_in.split("/"))
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
        {"title": "BnB Home", "available_rooms": available_rooms},
    )
