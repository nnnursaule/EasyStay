from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .models import Apartment, ResidentialComplex, ALL_AMENITIES, AMENITIES_TRANSLATION
from .forms import ApartmentForm
from django.views.generic import DetailView
class ResidentialComplexListView(ListView):
    model = ResidentialComplex
    template_name = "complex/complex_list.html"
    context_object_name = "complexes"


class ResidentialComplexDetailView(DetailView):
    model = ResidentialComplex
    template_name = "complex/complex_detail.html"
    context_object_name = "complex"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complex_instance = self.get_object()

        existing_amenities_raw = complex_instance.amenities.split(",") if complex_instance.amenities else []
        existing_amenities = [amenity.strip() for amenity in existing_amenities_raw]

        # Переводим ALL_AMENITIES в русский
        all_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in ALL_AMENITIES]

        # Определяем отсутствующие удобства
        missing_amenities = [amenity for amenity in all_amenities_ru if amenity not in existing_amenities]

        print("DetailView called!")
        print("Existing amenities:", existing_amenities)
        print("Missing amenities:", missing_amenities)

        context["existing_amenities"] = existing_amenities
        context["missing_amenities"] = missing_amenities
        return context