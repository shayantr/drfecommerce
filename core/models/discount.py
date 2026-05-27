from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.models.base_model import BaseModel

User = get_user_model()

class DiscountType(models.IntegerChoices):
    PERCENT = 1, 'Percent'
    AMOUNT = 2, 'Amount'

class Discount(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    value = models.IntegerField()
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountType.choices,
        default=DiscountType.AMOUNT
    )
    max_discount = models.IntegerField(
        null=True,
        blank=True,
        help_text="Only for percentage discounts"
    )

    min_order_amount = models.IntegerField(
        default=0
    )

    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table='discount'

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False, "inactive discount"
        if self.start_date and now < self.start_date:
            return False, "invalid discount"
        if self.end_date and now > self.end_date:
            return False, "invalid discount"
        return True, "valid"

    def show_value_str(self):
        if self.discount_type == DiscountType.PERCENT:
            if self.max_discount:
                return f'{self.value}% یا سقف {self.max_discount}'
            return f'{self.value}%'
        else:
            return self.value


    def calculate_discount(self, order_amount):
        if self.discount_type == DiscountType.PERCENT:
            discount = order_amount * (self.value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.value
        return discount



class DiscountUsage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user_order = models.ForeignKey('UserOrder', on_delete=models.CASCADE)
    class Meta:
        db_table='discount_usage'
        unique_together = ('user', 'discount', 'user_order')


