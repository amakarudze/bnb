from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CreateStaffForm, SignUpForm
from accounts.models import User, UserProfile


@login_required
@permission_required("accounts.add_staff", raise_exception=True)
def create_staff(request):
    form = CreateStaffForm()
    if request.method == "POST":
        form = CreateStaffForm(request.POST)

        try:
            # We need to do error handling in case the email already exist
            if form.is_valid():
                # Check if the form is valid before we save
                email = form.cleaned_data.get("email")
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                password1 = form.cleaned_data.get("password1")
                User.objects.create_staff(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1,
                )
                # Inform the user form was saved successfully.
                messages.success(request, "New Staff was created successfully")
                return redirect("website:home")
        except IntegrityError:
            messages.error(request, "The Staff has already been registered.")
    return render(
        request, "accounts/create_staff.html", {"form": form, "title": "Create Staff"}
    )


def signup(request):
    room = request.GET.get("room_id")
    if request.method == "POST":
        form = SignUpForm(request.POST)
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

            login(request, user)
            messages.success(request, "Sign-up successful!")

            if room:
                return redirect(reverse("website:make_reservation", args=(room.id)))
            else:
                return redirect("website:home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})
