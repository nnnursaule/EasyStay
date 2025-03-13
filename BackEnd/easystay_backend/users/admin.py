from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification

admin.site.register(User, UserAdmin)



@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("code", "expiration", "user")
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )