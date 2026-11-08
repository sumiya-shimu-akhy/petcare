import re
from django.db import models
from django.contrib.auth.models import User


class ProviderProfile(models.Model):
    SERVICE_TYPES = [
        ('vet', 'Veterinarian'),
        ('groomer', 'Groomer'),
        ('sitter', 'Pet Sitter'),
        ('trainer', 'Trainer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES)
    experience_years = models.PositiveIntegerField(default=0)
    fee = models.PositiveIntegerField(help_text="Fee in BDT per visit")
    area = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='provider_photos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube link of your demo video")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.get_service_type_display()}"

    @property
    def embed_url(self):
        url = (self.video_url or '').strip()
        match = re.search(r'(?:youtu\.be/|v=|embed/|shorts/)([A-Za-z0-9_-]{11})', url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return ''