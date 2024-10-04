# Create your views here.
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .forms import ReservationForm, GuestFormSet

def make_reservation_view(request):
    if request.method == 'POST':
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

            return redirect('reservation_success')  # Redirect to a success page

    else:
        reservation_form = ReservationForm()
        guest_formset = GuestFormSet(queryset=Guest.objects.none())  # Empty formset for guests

    return render(request, 'reservations/reservation.html', {
        'reservation_form': reservation_form,
        'guest_formset': guest_formset,
    })
