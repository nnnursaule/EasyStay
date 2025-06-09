from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    readonly_fields = ['student_id_preview']

    def student_id_preview(self, obj):
        if obj.student_id_photo:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.student_id_photo.url)
        return "No file uploaded"

    student_id_preview.short_description = "Student ID Preview"

    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'age', 'username', 'email', 'password',
                'phone_number', 'is_verified', 'is_landlord',
                'about', 'experience', 'image',
                'student_id_photo', 'student_id_preview', 'is_student_verified',
                'id_card_photo', 'ownership_doc', 'is_verified_landlord',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

admin.site.register(User, CustomUserAdmin)  # Используем кастомный UserAdmin




@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("code", "expiration", "user")
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )