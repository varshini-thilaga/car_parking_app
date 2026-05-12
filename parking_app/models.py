from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ParkingSlot(models.Model):
    ZONE_CHOICES = [
        ('A', 'Zone A'),
        ('B', 'Zone B'),
        ('C', 'Zone C'),
        ('D', 'Zone D'),
    ]
    
    slot_number = models.CharField(max_length=10, unique=True)
    zone = models.CharField(max_length=1, choices=ZONE_CHOICES, default='A')
    is_available = models.BooleanField(default=True)
    floor = models.IntegerField(default=1)
    price_per_hour = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['zone', 'floor', 'slot_number']

    def __str__(self):
        return f"Slot {self.slot_number} (Zone {self.zone}) - {'Available' if self.is_available else 'Occupied'}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='bookings')
    vehicle_number = models.CharField(max_length=20)
    booking_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_time']

    def __str__(self):
        return f"{self.user.username} - {self.slot.slot_number} - {self.vehicle_number}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    vehicle_color = models.CharField(max_length=20, blank=True)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bookings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}★"

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[('card', 'Card'), ('cash', 'Cash'), ('wallet', 'Wallet')])
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment #{self.id} - ${self.amount}"
