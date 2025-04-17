from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .models import Apartment, ResidentialComplex, ALL_AMENITIES, AMENITIES_TRANSLATION
from .forms import ApartmentForm
from django.views.generic import DetailView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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


def share_with_others(request):
    return render(request, "complex/share_with_others.html")


def main_page(request, pk):
    user = get_object_or_404(User, id=pk)
    complex = ResidentialComplex.objects.all()
    return render(request, 'bookings/index.html', {
        "user":user,
        "complexes": complex,
    })


class ApartmentCreateView(LoginRequiredMixin, CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'apartments/advertisement.html'
    success_url = reverse_lazy('apartment_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        return super().form_valid(form)



class ApartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'apartments/advertisement.html'
    success_url = reverse_lazy('booking:index')

    def get_queryset(self):
        return Apartment.objects.filter(landlord=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk  # Передаем ID пользователя
        return context
class ApartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    template_name = 'apartments/advertisement.html'
    success_url = reverse_lazy('apartment_list')

    def get_queryset(self):
        return Apartment.objects.filter(landlord=self.request.user)

def landlord_apartments(request, pk):
    apartments = Apartment.objects.filter(landlord_id=pk)
    return render(request, "apartments/advertisement.html", {
        "apartments": apartments,
    })


def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)

    if request.method == 'POST':
        # Если форма подтверждения удаления была отправлена
        apartment.delete()
        return redirect('booking:index')  # После удаления редиректим на список квартир

    return render(request, 'apartments/delete.html', {'apartment': apartment})