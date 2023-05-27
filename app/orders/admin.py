from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Register the Order model and settings fields for admin"""

    list_display = ('__str__', 'status')
    fields = (
        'id',
        'created',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history',
        'status',
        'initiator',
    )
    readonly_fields = ('id', 'created')
