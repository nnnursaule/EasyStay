from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Apartment, ResidentialComplex, Review, Favourite, Complaint, Feedback,
                     Booking, TopPromotion, PromotionOption, Notification, BookingDocument)

admin.site.register(Apartment)
admin.site.register(ResidentialComplex)
admin.site.register(Review)
admin.site.register(Favourite)
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(Booking)
admin.site.register(TopPromotion)
admin.site.register(Notification)
admin.site.register(BookingDocument)
@admin.register(PromotionOption)
class PromotionOptionAdmin(admin.ModelAdmin):
    list_display = ('duration', 'original_price', 'discounted_price', 'discount_percent')