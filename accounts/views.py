# Create your views here.
from django.shortcuts import render, redirect
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
