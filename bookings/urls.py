from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_bookings, name='my_bookings'),
    path('requests/', views.provider_requests, name='provider_requests'),
    path('new/<int:provider_id>/', views.booking_create, name='booking_create'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
]