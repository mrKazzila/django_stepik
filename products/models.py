import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)
    stripe_product_price_id = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    def create_stripe_model_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            unit_amount=round(self.price * 100),
            currency="rub",
            # recurring={"interval": "month"},
            product=stripe_product['id'],
        )
        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.stripe_product_price_id:
            stripe_product_price_id = self.create_stripe_model_price()
            self.stripe_product_price_id = stripe_product_price_id['id']

        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        return [
            {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            for basket in self
        ]


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    @property
    def sum(self):
        return self.product.price * self.quantity
