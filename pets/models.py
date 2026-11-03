from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    breed = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.pet_type})"