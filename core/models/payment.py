from django.db import models

from core.models.base_model import BaseModel

class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    FAILED = 3, 'Failed'

class Payment(BaseModel):
    order = models.ForeignKey('order', on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    ip_address = models.GenericIPAddressField()
    transaction_id = models.CharField(max_length=255)
    gateway = models.CharField(max_length=255)

    class Meta:
        db_table = 'payment'