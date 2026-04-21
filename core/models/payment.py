from django.db import models

from core.models.base_model import BaseModel

class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    FAILED = 3, 'Failed'

class Payment(BaseModel):
    class Meta:
        db_table = 'payment'
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey('userorder', on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    ip_address = models.GenericIPAddressField()
    transaction_id = models.CharField(max_length=255)
    gateway = models.CharField(max_length=255)

