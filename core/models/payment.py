from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.base_model import BaseModel


class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    FAILED = 3, 'Failed'

class Payment(BaseModel):
    class Meta:
        db_table = 'payment'
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    user_order = models.ForeignKey('UserOrder', on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    status = models.PositiveSmallIntegerField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    authority = models.CharField(max_length=255, unique=True)
    gateway = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)

@receiver(post_save, sender=Payment)
def create_payment_task(sender, instance, created, **kwargs):
    if created:
        from purchase.tasks import verify_payment

        transaction.on_commit(lambda:verify_payment.apply_async(
            args=[instance.id],
            countdown= 60 * 15 # check after 15 minutes
        ))
