# Create your views here.
from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm
from .models import User, UserProfile

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Create the user profile
            UserProfile.objects.create(
                user=user,
                dob=form.cleaned_data['dob'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                phone_number=form.cleaned_data['phone_number']
            )
            # Log in the user and redirect
            login(request, user)
            messages.success(request, 'Sign-up successful!')
            return redirect('some_dashboard_view')  # Redirect to a dashboard or another page after sign-up
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})
=======
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
>>>>>>> a50589a3cc94bfe63d93cab94fb15b97633a4ad0
