from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from . import forms
from .forms import ReservationForm, StaffReservationForm

from accounts.models import UserProfile, User


def dashboard(request):
    """Dashboard page for the staff reservation website"""
    return render(request, "reservations/index.html", {"title": "Home"})


def staff_sign_up_for_guest(request):
    form = StaffReservationForm()
    if request.method == "POST":
        form = StaffReservationForm(request.POST)
        if form.is_valid():
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
    else:
        form = StaffReservationForm()

    return render(request, "accounts/signup.html", {"form": form})


# reservation/views.py

@login_required
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
