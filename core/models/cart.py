from django.db import models
from django.db.models import Sum, F, Case, When

from .discount import Discount
from core.models.base_model import BaseModel

class UserCart(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cart_user')
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'user_cart'

    def calculate_total(self):
        return self.items.aggregate(
            total=Sum(
                F('quantity') * Case(
                    When(product__sale_price__isnull=False, then=F('product__sale_price')),
                    default=F('product__price'),
                )
            )
        )['total']

    def final_price(self):
        total = self.calculate_total()
        if self.discount_code:
            discount = Discount.objects.filter(code__iexact=self.discount_code).first()
            is_valid, _ = discount.is_valid()

            if is_valid:
                discount_amount = discount.calculate_discount(total)
                return total - discount_amount
        return total

class Cart(BaseModel):
    user_cart = models.ForeignKey('UserCart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    class Meta:
        db_table = 'cart'

    @property
    def total_price(self):
        if self.product.sale_price:
            return self.quantity * self.product.sale_price
        else:
            return self.quantity * self.product.price
