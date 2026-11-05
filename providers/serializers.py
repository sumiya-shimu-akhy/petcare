from rest_framework import serializers
from .models import ProviderProfile


class ProviderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = ProviderProfile
        fields = ['id', 'username', 'service_type', 'service_type_display',
                  'experience_years', 'fee', 'area', 'bio']