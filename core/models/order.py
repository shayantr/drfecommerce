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




class OrderItem(BaseModel):
    class Meta:
        db_table = 'order_item'

    product = models.ForeignKey('product', on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey('userorder', on_delete=models.CASCADE)



