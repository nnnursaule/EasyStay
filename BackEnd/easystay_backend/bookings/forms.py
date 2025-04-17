from django import forms
from .models import Apartment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['title', 'address', 'price_per_month', 'price_per_day',
                  'status', 'description', 'image']


