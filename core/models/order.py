from django.db import models

from core.models.base_model import BaseModel
from core.models.choices import OrderStatus


class Order(BaseModel):
    class Meta:
        db_table = 'order'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.IntegerField()
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, related_name='orders')




class OrderItem(BaseModel):
    class Meta:
        db_table = 'user_order'

    user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('product', on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey('order', on_delete=models.CASCADE)



