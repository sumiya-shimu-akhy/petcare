from django.urls import path
from . import views, api, match_views

urlpatterns = [
    path('', views.provider_list, name='provider_list'),
    path('profile/', views.provider_edit, name='provider_edit'),
    path('match/', match_views.provider_match, name='provider_match'),
    path('api/', api.ProviderListAPI.as_view(), name='provider_api'),
    path('api/<int:pk>/', api.ProviderDetailAPI.as_view(), name='provider_api_detail'),
    path('<int:pk>/', views.provider_detail, name='provider_detail'),
]