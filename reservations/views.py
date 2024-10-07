from django.shortcuts import render


def dashboard(request):
    """Dashboard page for the staff reservation website"""
    return render(request, "reservations/index.html", {"title": "Home"})
