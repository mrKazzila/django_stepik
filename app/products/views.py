from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from config.settings import LOGIN_URL
from .models import Basket, Product, ProductCategory
from .product_services import update_or_add_to_basket


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    title = 'Store - Catalog'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category__id=category_id) if category_id is not None else queryset


@login_required(login_url=LOGIN_URL)
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)

    update_or_add_to_basket(
        user=request.user,
        basket_obj=Basket.objects.filter(user=request.user, product=product),
        product_obj=Product.objects.get(id=product_id),
        basket_model=Basket,
    )

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url=LOGIN_URL)
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
