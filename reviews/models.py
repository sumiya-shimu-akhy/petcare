from django.db import models
from django.contrib.auth.models import User
from providers.models import ProviderProfile


class Review(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.provider} ({self.rating}/5)"


class Reaction(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField()  # 1 = like, -1 = dislike

    class Meta:
        unique_together = ('provider', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.provider} ({self.value})"