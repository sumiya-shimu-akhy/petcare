from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Pet Owner'),
        ('provider', 'Service Provider'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    phone_verified = models.BooleanField(default=False)
    area = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.username}"


class PhoneOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    attempts = models.PositiveSmallIntegerField(default=0)
    sent_count = models.PositiveSmallIntegerField(default=0)
    window_start = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Phone OTP for {self.user.username}"


class SmsLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS sent at {self.created_at:%Y-%m-%d %H:%M}"