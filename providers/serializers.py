from django.db.models import Avg
from rest_framework import serializers

from .models import ProviderProfile


class ProviderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    photo = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = ProviderProfile
        fields = ['id', 'username', 'service_type', 'service_type_display',
                  'experience_years', 'fee', 'area', 'bio',
                  'photo', 'average_rating', 'review_count']

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(a=Avg('rating'))['a']
        return round(avg, 1) if avg else None

    def get_review_count(self, obj):
        return obj.reviews.count()