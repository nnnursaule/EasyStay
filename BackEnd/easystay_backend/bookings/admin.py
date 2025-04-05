from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Apartment, ResidentialComplex, Review

admin.site.register(Apartment)
admin.site.register(ResidentialComplex)
admin.site.register(Review)