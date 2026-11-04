from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pets/', include('pets.urls')),
    path('providers/', include('providers.urls')),
    path('reviews/', include('reviews.urls')),
    path('bookings/', include('bookings.urls')),
    path('', include('accounts.urls')),
]