from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q, Sum, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from .models import ParkingSlot, Booking, UserProfile, Review, SupportTicket, Payment
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle_number', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'description', 'priority']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'vehicle_color']

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    stats = {
        'total_slots': ParkingSlot.objects.count(),
        'available_slots': ParkingSlot.objects.filter(is_available=True).count(),
        'total_bookings': Booking.objects.count(),
    }
    return render(request, 'home.html', stats)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    slots = ParkingSlot.objects.all()
    bookings = Booking.objects.filter(user=request.user).select_related('slot')
    active_booking = bookings.filter(status='active').first()
    
    stats = {
        'total_bookings': bookings.count(),
        'active_bookings': bookings.filter(status='active').count(),
        'completed_bookings': bookings.filter(status='completed').count(),
        'available_slots': ParkingSlot.objects.filter(is_available=True).count(),
        'total_slots': ParkingSlot.objects.count(),
    }
    
    return render(request, 'dashboard.html', {
        'slots': slots,
        'bookings': bookings,
        'active_booking': active_booking,
        'stats': stats,
    })

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)
    
    if not slot.is_available:
        messages.error(request, "Slot is not available.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.slot = slot
            booking.status = 'active'
            
            hours = (booking.end_time - booking.start_time).total_seconds() / 3600
            booking.amount_paid = float(slot.price_per_hour) * max(1, hours)
            booking.save()
            
            slot.is_available = False
            slot.save()
            
            messages.success(request, f"Slot {slot.slot_number} booked successfully!")
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
        form.fields['start_time'].initial = timezone.now()
        form.fields['end_time'].initial = timezone.now() + timedelta(hours=2)
    
    return render(request, 'booking.html', {'slot': slot, 'form': form})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    review_exists = Review.objects.filter(booking=booking).exists()
    
    if request.method == 'POST' and not review_exists:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.booking = booking
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        review_form = ReviewForm()
    
    return render(request, 'booking_detail.html', {
        'booking': booking,
        'review_form': review_form,
        'review_exists': review_exists,
    })

@login_required
def release_slot(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.slot.is_available = True
    booking.slot.save()
    booking.status = 'completed'
    booking.save()
    messages.success(request, "Slot released successfully!")
    return redirect('dashboard')

@login_required
def parking_map(request):
    zones = ParkingSlot.ZONE_CHOICES
    slots_by_zone = {}
    for zone_code, zone_name in zones:
        slots_by_zone[zone_code] = ParkingSlot.objects.filter(zone=zone_code).order_by('floor', 'slot_number')
    
    total_available = ParkingSlot.objects.filter(is_available=True).count()
    total_occupied = ParkingSlot.objects.filter(is_available=False).count()
    total_slots = total_available + total_occupied
    occupancy = (total_occupied / total_slots * 100) if total_slots > 0 else 0
    
    stats = {
        'total_available': total_available,
        'total_occupied': total_occupied,
        'occupancy_percentage': round(occupancy, 1),
    }
    
    return render(request, 'parking_map.html', {
        'zones_data': slots_by_zone,
        'stats': stats,
    })

@login_required
def history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('slot')
    
    stats = {
        'total_hours': sum((b.end_time - b.start_time).total_seconds() / 3600 
                          for b in bookings if b.end_time) if bookings else 0,
        'total_spent': bookings.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0,
        'completed': bookings.filter(status='completed').count(),
    }
    
    return render(request, 'history.html', {
        'bookings': bookings,
        'stats': stats,
    })

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    
    stats = {
        'total_bookings': Booking.objects.filter(user=request.user).count(),
        'total_spent': Booking.objects.filter(user=request.user).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0,
        'avg_rating': Review.objects.filter(user=request.user).aggregate(Avg('rating'))['rating__avg'] or 0,
    }
    
    return render(request, 'user_profile.html', {
        'form': form,
        'profile': profile,
        'stats': stats,
    })

@login_required
def support(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Support ticket created successfully!')
            return redirect('support_detail', ticket_id=ticket.id)
    else:
        form = SupportTicketForm()
    
    return render(request, 'support.html', {
        'tickets': tickets,
        'form': form,
    })

@login_required
def support_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    return render(request, 'support_detail.html', {'ticket': ticket})

@login_required
def pricing(request):
    slots = ParkingSlot.objects.values('zone').annotate(
        count=Count('id'),
        available=Count('id', filter=Q(is_available=True)),
        price=F('price_per_hour')
    ).distinct()
    
    pricing_info = {
        'zones': ParkingSlot.objects.values_list('zone', flat=True).distinct(),
        'avg_price': ParkingSlot.objects.aggregate(Avg('price_per_hour'))['price_per_hour__avg'] or 0,
    }
    
    return render(request, 'pricing.html', {'pricing_info': pricing_info})

@login_required
def reviews(request):
    user_reviews = Review.objects.filter(user=request.user).select_related('booking', 'booking__slot')
    avg_rating = user_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'reviews.html', {
        'reviews': user_reviews,
        'avg_rating': avg_rating,
    })

def get_slot_status(request):
    slots = ParkingSlot.objects.all().values('id', 'slot_number', 'zone', 'is_available', 'floor')
    return JsonResponse(list(slots), safe=False)
