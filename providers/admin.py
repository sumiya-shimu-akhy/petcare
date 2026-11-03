from django.contrib import admin
from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'area', 'fee', 'is_verified')
    list_filter = ('service_type', 'is_verified')