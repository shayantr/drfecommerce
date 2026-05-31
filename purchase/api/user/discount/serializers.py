from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DJValidationError

from core.models import Discount, UserCart


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
        try:
            discount.validate(
                total=total,
            )
        except DJValidationError as e:
            raise ValidationError(str(e))
        user_cart.discount_code = discount.code
        user_cart.save()
        return validated_data