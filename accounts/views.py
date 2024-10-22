from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import CreateStaffForm, SignUpForm
from accounts.models import User, UserProfile


FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


def send_email(subject, message, from_email, to_email):
    send_mail(
        subject,
        message,
        from_email,
        to_email,
        fail_silently=False,
    )


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
                message = render_to_string(
                    "emails/new_staff_account_confirmation.html",
                    {"name": first_name, "username": email},
                )
                from_email = FROM_EMAIL
                to_email = [email]
                subject = "Your BnB account is created!"
                # Inform the user form was saved successfully.
                send_email(subject, message, from_email, to_email)
                messages.success(request, "New Staff was created successfully")
                return redirect("website:home")
        except IntegrityError:
            messages.error(request, "The Staff has already been registered.")
    return render(
        request, "accounts/create_staff.html", {"form": form, "title": "Create Staff"}
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
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
                message = render_to_string(
                    "emails/guest_signup_confirmation.html",
                    {"name": user.first_name, "username": user.email},
                )
                authenticated_user = authenticate(
                    request, username=email, password=password
                )
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    reverse("website:make_reservation")

                from_email = FROM_EMAIL
                to_email = [user.email]
                subject = "Thank you for signing up at BnB!"
                send_email(subject, message, from_email, to_email)

                messages.success(request, "Sign-up successful!")

            except IntegrityError:
                messages.error(request, "User already exist!")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})
