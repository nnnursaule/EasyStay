from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .models import Apartment, ResidentialComplex
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

def apartment_management(request):
    apartments = Apartment.objects.filter(landlord=request.user)
    return render(request, 'apartments/apartment_management.html', {'apartments': apartments})


def apartment_detail(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, landlord=request.user)
    return render(request, 'apartments/apartment_detail.html', {'apartment': apartment})



def apartment_create(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.landlord = request.user
            apartment.save()
            return redirect('apartment_management')
    else:
        form = ApartmentForm()
    return render(request, 'apartments/apartment_form.html', {'form': form, 'title': 'Добавить квартиру'})


def apartment_edit(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, landlord=request.user)
    if request.method == "POST":
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return redirect('apartment_detail', apartment_id=apartment.id)
    else:
        form = ApartmentForm(instance=apartment)
    return render(request, 'apartments/apartment_form.html', {'form': form, 'title': 'Редактировать квартиру'})


def apartment_delete(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, landlord=request.user)
    apartment.delete()
    return redirect('apartment_management')