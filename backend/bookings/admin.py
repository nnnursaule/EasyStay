from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Apartment, ResidentialComplex, Review, Favourite, Complaint, Feedback,
                     Booking, TopPromotion, PromotionOption, Notification, BookingDocument, ApartmentImage)


admin.site.register(ResidentialComplex)
admin.site.register(Review)
admin.site.register(Favourite)
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(Booking)
admin.site.register(TopPromotion)
admin.site.register(Notification)
admin.site.register(BookingDocument)
class ApartmentImageInline(admin.TabularInline):  # или admin.StackedInline
    model = ApartmentImage
    extra = 1  # сколько пустых форм показывать
    max_num = 10  # максимум изображений можно загрузить

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]
@admin.register(PromotionOption)
class PromotionOptionAdmin(admin.ModelAdmin):
    list_display = ('duration', 'original_price', 'discounted_price', 'discount_percent')