from django.urls import path
from . import views

urlpatterns = [
    path('<int:provider_id>/', views.reviews_json, name='reviews_json'),
    path('<int:provider_id>/add/', views.add_review, name='add_review'),
    path('<int:provider_id>/reactions/', views.reactions_json, name='reactions_json'),
    path('<int:provider_id>/react/', views.react, name='react'),
]