import enum

from django.db import models

from products.models import Basket
from users.models import User


class OrderStatus(enum.Enum):
    CREATED = 'Создан'
    PAID = 'Оплачен'
    ON_WAY = 'В пути'
    DELIVERED = 'Доставлен'


# Create your models here.
class Order(models.Model):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.CharField(max_length=256)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in OrderStatus],
        default=OrderStatus.CREATED.name,
    )
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = OrderStatus.PAID.name
        self.basket_history = {
            'purchased_items': [basket.do_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
