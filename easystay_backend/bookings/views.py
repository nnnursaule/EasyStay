from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .models import Apartment, ResidentialComplex, ALL_AMENITIES, AMENITIES_TRANSLATION, Favourite
from .forms import ApartmentForm
from django.views.generic import DetailView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class ApartmentListView(ListView):
    model = Apartment
    template_name = "complex/apartment_list.html"
    context_object_name = "apartments"


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = "complex/apartment_details.html"
    context_object_name = "apartment"  # Изменил название на apartment, чтобы было понятно, что это квартира

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartment = self.object

        existing_amenities = apartment.amenities or []

        # Переводим ALL_AMENITIES в русский
        all_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in ALL_AMENITIES]
        existing_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in existing_amenities]

        # Определяем отсутствующие удобства
        missing_amenities = [amenity for amenity in all_amenities_ru if amenity not in existing_amenities_ru]

        context["existing_amenities"] = existing_amenities_ru
        context["missing_amenities"] = missing_amenities
        return context


def share_with_others(request):
    return render(request, "complex/share_with_others.html")


def main_page(request, pk):
    user = get_object_or_404(User, id=pk)
    apartments = Apartment.objects.filter(status="available")  # Только доступные

    # Забираем фильтры из формы
    city = request.GET.get("city")
    complex_id = request.GET.get("complex_id")
    max_price = request.GET.get("max_price")
    room_count = request.GET.get("room_count")
    rental_type = request.GET.get("rental_type")

    # Применяем фильтры
    if city:
        apartments = apartments.filter(complex__city__icontains=city)

    if complex_id:
        apartments = apartments.filter(complex_id=complex_id)

    if max_price:
        if rental_type == "month":
            apartments = apartments.filter(price_per_month__lte=max_price)
        elif rental_type == "day":
            apartments = apartments.filter(price_per_day__lte=max_price)

    if room_count:
        if room_count == "4":
            apartments = apartments.filter(room_count__gte=4)
        else:
            apartments = apartments.filter(rooms=room_count)

    complexes = ResidentialComplex.objects.all()

    return render(request, "bookings/index.html", {
        "user": user,
        "apartments": apartments,
        "complexes": complexes,
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


def remove_from_favourites(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    Favourite.objects.filter(user=request.user, apartment=apartment).delete()
    return redirect('booking:favourites')  # Перенаправление на страницу избранных квартир

def favourites_view(request):
    # Получаем все избранные квартиры текущего пользователя
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'bookings/favourites.html', {'favourites': favourites})

def add_to_favourites(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    if not Favourite.objects.filter(user=request.user, apartment=apartment).exists():
        Favourite.objects.create(user=request.user, apartment=apartment)
    return redirect('all_apartments')

def toggle_favourite(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    fav, created = Favourite.objects.get_or_create(user=request.user, apartment=apartment)

    if not created:
        fav.delete()  # Если уже в избранном — удаляем
    return redirect(request.META.get('HTTP_REFERER', 'favourites'))