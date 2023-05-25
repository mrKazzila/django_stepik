from django.contrib import admin

from .models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = (
        'name', 'description',
        'category', ('price', 'quantity'),
        'stripe_product_price_id', 'image',
    )

    search_fields = ('name', 'quantity', 'category')
    ordering = ('price', 'quantity', 'category')


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
