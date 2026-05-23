from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
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
    used_count = models.PositiveIntegerField(default=0)

    users = models.ManyToManyField(
        to=User,
        through= 'DiscountUser',
        related_name='users',
        blank=True,
        help_text="If empty, available for all users"
    )

    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    products = models.ManyToManyField(
        to='core.Product',
        through= 'DiscountProduct',
        related_name='products',
        blank=True,
        help_text="If empty, available for all products"
    )
    categories = models.ManyToManyField(
        to='core.Category',
        through='DiscountCategory',
        related_name='categories',
        blank=True,
        help_text="If empty, available for all categories"
    )
    exclude_products = models.ManyToManyField(
        to='core.Product',
        through='ExcludeDiscountProduct',
        related_name='exclude_products',
        blank=True,
        help_text="If empty, available for all excluded products"
    )

    def is_valid(self, user=None, order_amount=None):
        now = timezone.now()
        if self.users.exists() and user not in self.users.all():
            return False, 'not_allowed'
        if not self.is_active:
            return False, "inactive discount"
        if self.start_date and now < self.start_date:
            return False, "invalid discount"
        if self.end_date and now > self.end_date:
            return False, "invalid discount"
        if order_amount and order_amount < self.min_order_amount:
            return False, "invalid discount"
        if self.usage_limit and self.used_count > self.usage_limit:
            return False, "invalid discount"
        return True, "valid"


    def calculate_discount(self, order_amount=None):
        if self.discount_type == DiscountType.PERCENT:
            discount = order_amount * (self.value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.value
        return discount

class DiscountUser(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'discount_id')
        db_table = 'discount_users'

class DiscountProduct(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_id', 'discount_id')
        db_table = 'discount_products'
class DiscountCategory(models.Model):
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category_id', 'discount_id')
        db_table = 'discount_categories'
class ExcludeDiscountProduct(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('product_id', 'discount_id')
        db_table = 'exclude_discount_products'