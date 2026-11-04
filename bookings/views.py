from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from providers.models import ProviderProfile
from .forms import BookingForm
from .models import Booking


@login_required
def booking_create(request, provider_id):
    provider = get_object_or_404(ProviderProfile, pk=provider_id, is_verified=True)
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.provider = provider
            booking.owner = request.user
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(user=request.user)
    return render(request, 'bookings/booking_form.html', {'form': form, 'provider': provider})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(owner=request.user).select_related('provider__user', 'pet')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def provider_requests(request):
    profile = ProviderProfile.objects.filter(user=request.user).first()
    if profile:
        bookings = Booking.objects.filter(provider=profile).select_related('owner', 'pet')
    else:
        bookings = Booking.objects.none()
    return render(request, 'bookings/provider_requests.html', {'bookings': bookings, 'profile': profile})


@login_required
@require_POST
def update_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk, provider__user=request.user)
    action = request.POST.get('action')
    if action == 'accept':
        booking.status = 'accepted'
        booking.save()
    elif action == 'reject':
        booking.status = 'rejected'
        booking.save()
    return redirect('provider_requests')