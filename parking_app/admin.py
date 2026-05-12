from django.contrib import admin
from .models import ParkingSlot, Booking, UserProfile, Review, SupportTicket, Payment

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'zone', 'floor', 'is_available', 'price_per_hour')
    list_filter = ('zone', 'floor', 'is_available')
    search_fields = ('slot_number',)
    ordering = ('zone', 'floor', 'slot_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slot', 'vehicle_number', 'status', 'amount_paid', 'booking_time')
    list_filter = ('status', 'booking_time', 'slot__zone')
    search_fields = ('user__username', 'vehicle_number', 'slot__slot_number')
    readonly_fields = ('booking_time',)
    ordering = ('-booking_time',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'total_bookings', 'total_spent', 'created_at')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('user__username', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_date', 'method')
    list_filter = ('method', 'payment_date')
    search_fields = ('transaction_id', 'booking__user__username')
    readonly_fields = ('payment_date',)
