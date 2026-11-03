from django import forms
from .models import ProviderProfile


class ProviderForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['service_type', 'experience_years', 'fee', 'area', 'bio']