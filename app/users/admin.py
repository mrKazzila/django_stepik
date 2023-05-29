from django.contrib import admin

from products.admin import BasketAdmin
from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Register the User model and settings fields for admin"""

    list_display = ('username',)
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Register the EmailVerification model and settings fields for admin"""

    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'expiration', 'created')
    readonly_fields = ('created',)
