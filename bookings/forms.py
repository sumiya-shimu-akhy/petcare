from datetime import date
from django import forms
from pets.models import Pet
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pet', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(owner=user)
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

    def clean_date(self):
        chosen = self.cleaned_data['date']
        if chosen < date.today():
            raise forms.ValidationError("Please choose today or a future date.")
        return chosen