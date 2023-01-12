from django.shortcuts import render
from products.models import Product, ProductCategory

# Create your views here.


def index(request):
    context = {
        'title': 'Store',  # Placeholder
    }
    return render(request=request, template_name='products/index.html', context=context)


def products(request):
    context = {
        'title': 'Store - Каталог',  # Placeholder
        'products': Product.objects.all(),
        'category': ProductCategory.objects.all(),
    }
    return render(request=request, template_name='products/products.html', context=context)
