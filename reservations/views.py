from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse

from .models import Reservation, Guest
from .forms import ReservationsUpdateForm, GuestFormSet, AddReservationForm

from accounts.models import UserProfile, User


@login_required
def dashboard(request):
    """Dashboard page for the staff reservation website"""
    return render(request, "reservations/index.html", {"title": "Home"})


@login_required
@permission_required("reservations.view_reservation", raise_exception=True)
def reservations_list(request):
    reservations = (
        Reservation.objects.prefetch_related("guest_set")
        .all()
        .order_by("-check_in_date")
    )
    return render(
        request,
        "reservations/reservations_list.html",
        {"title": "Reservations List", "reservations": reservations},
    )


class UpdateReservationsView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationsUpdateForm
    template_name = "website/reservation.html"
    permission_required = "reservations.change_reservations"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse("reservations:reservations_list")

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Reservation"
        context["guest_formset"] = GuestFormSet()
        return context


@login_required
def add_reservation(request):
    form = AddReservationForm()
    if request.method == "POST":
        form = AddReservationForm(request.POST)
        guest_formset = GuestFormSet(request.POST)
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
            reservation = Reservation.objects.create(
            user=user,
            number_of_adults=form.cleaned_data.get("number_of_adults"),
            number_of_children=form.cleaned_data.get("number_of_children"),
            rooms=form.cleaned_data.get("rooms"),
            events=form.cleaned_data.get("event"),
            check_in_date=form.cleaned_data.get("check_in_date"),
            check_out_date=form.cleaned_data.get("check_out_date"),
              )
        if guest_formset.is_valid():
             for guest_form in guest_formset:
                if guest_form.cleaned_data:  
                    guest = guest_form.save(commit=False)
                    guest.reservation = reservation
                    guest.save()
        messages.success(request, "New reservation added successfully")
        return redirect("reservations:reservations_list")
        
    else:
        form = AddReservationForm()
    return render(request, "reservations/reservation.html", {"form": form, "guest_formset": guest_formset})


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Check if the reservation is already canceled
    if reservation.is_cancelled:
        return HttpResponse("This reservation is already canceled.")

    # Mark the reservation as canceled
    reservation.is_cancelled = True
    reservation.save()