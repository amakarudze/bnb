# Create your views here.
from django.shortcuts import render, redirect
from .forms import CreateStaffForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import IntegrityError

from accounts.models import User


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
