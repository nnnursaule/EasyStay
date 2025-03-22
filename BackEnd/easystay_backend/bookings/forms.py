from django import forms
from .models import Apartment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['title','complex', 'rooms', 'area', 'floor', 'price_per_month', 'image']
