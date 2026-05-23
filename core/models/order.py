from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.base_model import BaseModel


class OrderStatus(models.IntegerChoices):
    CANCELLED = 1, 'Cancelled'
    PENDING = 2, 'Pending'
    RETURNED = 3, 'Returned'
    COMPLETED = 4, 'Completed'
    DELIVERED = 5, 'Delivered'
    AWAITING_PAYMENT = 6, 'Awaiting Payment'


class UserOrder(BaseModel):
    class Meta:
        db_table = 'user_order'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_orders')
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.AWAITING_PAYMENT)
    total_amount = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, related_name='user_orders')
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, related_name='user_orders', blank=True, null=True)

@receiver(post_save, sender=UserOrder)
def create_order_task(sender, instance, created, **kwargs):
    if created:
        from purchase.tasks import check_order_status

        transaction.on_commit(lambda: check_order_status.apply_async(
            args=[instance.id],
            countdown=60 * 60
        ))


class Order(BaseModel):
    class Meta:
        db_table = 'order'

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey('UserOrder', on_delete=models.CASCADE, related_name='orders')


