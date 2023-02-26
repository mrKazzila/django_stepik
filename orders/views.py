from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from orders.order_services import (create_checkout_session,
                                   handle_stripe_webhook)
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    title = 'Store - спасибо за заказ'
    template_name = 'orders/success.html'


class CanceledTemplateView(TitleMixin, TemplateView):
    title = 'Store - заказ не принят!'
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        try:
            checkout_session = create_checkout_session(
                line_items=baskets.stripe_products(),
                order_id=self.object.id,
                success_page=f"{settings.DOMAIN_NAME}{reverse('orders:order_success')}",
                cancel_page=f"{settings.DOMAIN_NAME}{reverse('orders:order_canceled')}",
            )
        except Exception as e:
            return str(e)

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - заказы'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ №{self.object.id}'
        return context


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    handle_stripe_webhook(
        payload=payload,
        sig_header=sig_header,
        order_model=Order,
    )

    return HttpResponse(status=200)
