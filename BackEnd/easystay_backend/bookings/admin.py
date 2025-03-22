from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Apartment, ResidentialComplex

admin.site.register(Apartment)
admin.site.register(ResidentialComplex)