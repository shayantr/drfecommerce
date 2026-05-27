from rest_framework.exceptions import ValidationError

from core.models import Product, Discount
from core.models.discount import DiscountUsage


def restore_product_reservation(item):
    product = Product.objects.select_for_update().filter(pk=item.product.pk).first()
    product.quantity += item.quantity
    product.save()

class DiscountService:
    @staticmethod
    def validate(discount: Discount, total):
        if not discount.is_valid:
            raise ValidationError("Invalid discount")
        if discount.min_order_amount & total < discount.min_order_amount:
            raise ValidationError('min order amount required')

        usage_count = DiscountUsage.objects.filter(
            discount=discount,
        ).count()
        if discount.usage_limit and usage_count >=discount.usage_limit:
            raise ValidationError('usage limit reached')
        return True