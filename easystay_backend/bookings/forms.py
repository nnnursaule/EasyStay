from django import forms
from .models import Apartment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['title', 'address', 'price_per_month', 'price_per_day',
                  'status', 'description', 'image']


class ApartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'title', 'address', 'complex', 'rooms', 'area', 'floor',
            'price_per_month', 'price_per_day', 'status', 'description',
            'image', 'bathrooms', 'latitude', 'longitude',
            'min_age', 'max_age', 'musical_instruments',
            'gender_preference', 'pets_allowed', 'tenant_type',
            'smoking_policy', 'guest_policy', 'amenities'
        ]