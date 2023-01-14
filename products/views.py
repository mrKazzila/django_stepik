from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect

from products.models import Basket, Product, ProductCategory
# Create your views here.
from store.settings import LOGIN_URL
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store',  # Placeholder
    }
    return render(request=request, template_name='products/index.html', context=context)


def products(request, category_id=None, page_number=1):
    products = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
    }
    return render(request=request, template_name='products/products.html', context=context)


@login_required(login_url=LOGIN_URL)
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = Basket.objects.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url=LOGIN_URL)
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
