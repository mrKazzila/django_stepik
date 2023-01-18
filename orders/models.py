# import enum

from django.db import models
from users.models import User

#
# class OrderStatus(enum.Enum):
#     CREATED = 0
#     PAID = 1
#     ON_WAY = 2
#     DELIVERED = 3


# Create your models here.
class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.CharField(max_length=256)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.__class__.__name__} #{self.id}. {self.first_name} {self.last_name}'

