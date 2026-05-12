from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('release/<int:booking_id>/', views.release_slot, name='release_slot'),
    path('map/', views.parking_map, name='parking_map'),
    path('history/', views.history, name='history'),
    path('profile/', views.user_profile, name='user_profile'),
    path('support/', views.support, name='support'),
    path('support/<int:ticket_id>/', views.support_detail, name='support_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('reviews/', views.reviews, name='reviews'),
    path('api/slots-status/', views.get_slot_status, name='slots_status'),
]