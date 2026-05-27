from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Discount, UserCart
from purchase.service.product_services import DiscountService


class ApplyDiscountSerializer(serializers.Serializer):
    discount_code = serializers.CharField(required=True)

    def validate_discount_code(self, value):
        try:
            Discount.objects.get(code=value)
        except Discount.DoesNotExist:
            raise ValidationError("Discount code does not exist")
        return value

    def create(self, validated_data):
        discount = Discount.objects.get(code=validated_data.get('discount_code'))
        user = self.context['request'].user
        user_cart = UserCart.objects.get(user=user)
        total = user_cart.calculate_total()
        DiscountService.validate(
            user=user,
            total=total,
            discount=discount,
        )
        user_cart.discount_code = discount.code
        user_cart.save()
        return validated_data