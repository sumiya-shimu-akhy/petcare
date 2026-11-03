from django.urls import path
from . import views

urlpatterns = [
    path('', views.provider_list, name='provider_list'),
    path('profile/', views.provider_edit, name='provider_edit'),
]