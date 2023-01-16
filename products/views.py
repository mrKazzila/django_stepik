from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
# Create your views here.
from store.settings import LOGIN_URL
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category__id=category_id) if category_id is not None else queryset


# class BasketCreateView(CreateView):
#     model = Basket
#
#     def post(self, request, *args, **kwargs):
#         product = Product.objects.get(id=self.kwargs.get("product_id"))
#         baskets = Basket.objects.filter(user=request.user, product=product)
#
#         if not baskets.exists():
#             Basket.objects.create(user=request.user, product=product, quantity=1)
#         else:
#             basket = Basket.objects.first()
#             basket.quantity += 1
#             basket.save()
#
#         return HttpResponseRedirect(request.META['HTTP_REFERER'])


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
