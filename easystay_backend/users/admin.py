from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'favourites', 'age', 'username', 'email', 'password', 'phone_number', 'is_verified', 'is_landlord', 'about', 'experience', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # Убрали 'date_joined'
    )

admin.site.register(User, CustomUserAdmin)  # Используем кастомный UserAdmin




@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("code", "expiration", "user")
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )