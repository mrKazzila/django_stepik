from django.contrib import admin

from .models import Basket, Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Register the ProductCategory model for admin"""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Register the Product model and settings fields for admin"""

    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        'name',
        'description',
        'category',
        ('price', 'quantity'),
        'stripe_product_price_id',
        'image',
    )

    search_fields = ('name', 'quantity', 'category')
    ordering = ('price', 'quantity', 'category')


class BasketAdmin(admin.TabularInline):
    """Register the Basket model and settings fields for admin"""

    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
