from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from config.settings import LOGIN_URL
from .models import Basket, Product, ProductCategory
from .product_services import delete_user_basket, update_or_add_to_basket
import logging

logger = logging.getLogger(__name__)


class IndexView(TitleMixin, TemplateView):
    """Main page"""

    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    """Catalog with products"""

    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Catalog'
    slide_range = range(1, 6)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['slide_range'] = self.slide_range
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category__id=category_id) if category_id is not None else queryset


@login_required(login_url=LOGIN_URL)
def basket_add(request, product_id):
    """Add product to user basket"""
    product = Product.objects.get(id=product_id)
    basket_object = Basket.objects.filter(user=request.user, product=product)
    logger.info(f'Add basket_add: {product}')

    update_or_add_to_basket(
        user=request.user,
        basket_obj=basket_object,
        product_obj=product,
        basket_model=Basket,
    )

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url=LOGIN_URL)
def basket_remove(request, basket_id):
    """Remove user basket"""
    delete_user_basket(basket_model=Basket, basket_id=basket_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
