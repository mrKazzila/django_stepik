import stripe
from django.conf import settings
from django.db import models

from users.models import User
from .product_services import create_basket_item_json

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    """Category for product"""

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Product"""

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.PROTECT,
    )
    stripe_product_price_id = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Product: {self.name} | Category: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)

        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub',
        )

        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    """QuerySet for Basket model"""

    def total_sum(self):
        return sum(basket.sum for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        stripe_prod = []

        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            stripe_prod.append(item)

        return stripe_prod


class Basket(models.Model):
    """Basket"""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Cart for {self.user.username} | product: {self.product.name}'

    @property
    def sum(self):  # noqa A003
        return self.product.price * self.quantity

    def do_json(self):
        return create_basket_item_json(
            product_name=self.product.name,
            quantity=self.quantity,
            price=float(self.product.price),
            _sum=float(self.sum),
        )
