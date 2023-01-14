from django.contrib import admin

# Register your models here.
from products.models import ProductCategory, Product, Basket

# admin.site.register(Product)
admin.site.register(ProductCategory)
# admin.site.register(Basket)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category',)
    fields = ('name', 'description', 'category', ('price', 'quantity',), 'image',)
    readonly_fields = ('description',)
    search_fields = ('name', 'quantity', 'category',)
    ordering = ('price', 'quantity', 'category',)


# @admin.register(Basket)
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
