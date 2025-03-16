from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Apartment


def index(request):
    apartments = Apartment.objects.all()
    return render(request, "bookings/index.html", {
        "apartments": apartments,
    })


