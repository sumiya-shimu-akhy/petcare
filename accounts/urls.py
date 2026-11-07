from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('verify/resend/', views.resend_otp, name='resend_otp'),
    path('check-username/', views.check_username, name='check_username'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]