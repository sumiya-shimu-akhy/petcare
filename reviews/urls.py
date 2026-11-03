from django.urls import path
from . import views

urlpatterns = [
    path('<int:provider_id>/', views.reviews_json, name='reviews_json'),
    path('<int:provider_id>/add/', views.add_review, name='add_review'),
]