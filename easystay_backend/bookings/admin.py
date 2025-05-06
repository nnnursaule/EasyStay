from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Apartment, ResidentialComplex, Review, Favourite, Complaint, Feedback, Booking

admin.site.register(Apartment)
admin.site.register(ResidentialComplex)
admin.site.register(Review)
admin.site.register(Favourite)
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(Booking)