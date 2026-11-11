from django.urls import path
from django.views.generic import TemplateView
from . import views, api, match_views, chat_views

urlpatterns = [
    path('', views.provider_list, name='provider_list'),
    path('browse/', TemplateView.as_view(template_name='providers/provider_browse.html'), name='provider_browse'),
    path('profile/', views.provider_edit, name='provider_edit'),
    path('match/', match_views.provider_match, name='provider_match'),
    path('chat/', chat_views.chat_page, name='chat_page'),
    path('chat/api/', chat_views.chat_api, name='chat_api'),
    path('api/', api.ProviderListAPI.as_view(), name='provider_api'),
    path('api/<int:pk>/', api.ProviderDetailAPI.as_view(), name='provider_api_detail'),
    path('<int:pk>/', views.provider_detail, name='provider_detail'),
]