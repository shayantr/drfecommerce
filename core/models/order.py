from django.db import models
from core.models.base_model import BaseModel


class OrderStatus(models.IntegerChoices):
    CANCELLED = 1, 'Cancelled'
    PENDING = 2, 'Pending'
    RETURNED = 3, 'Returned'
    COMPLETED = 4, 'Completed'
    DELIVERED = 5, 'Delivered'


class UserOrder(BaseModel):
    class Meta:
        db_table = 'user_order'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.IntegerField()
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, related_name='orders')


class Order(BaseModel):
    class Meta:
        db_table = 'order'

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey('UserOrder', on_delete=models.CASCADE, related_name='orders')

