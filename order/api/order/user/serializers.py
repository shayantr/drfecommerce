from django.db import transaction
from rest_framework import serializers

from core.models import Order, Cart, UserOrder, UserCart, Product


class UserOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'total_amount', 'address']
        read_only_fields = ('id', 'status', 'total_amount')

    def _buy_product(self, product, quantity):
        product = Product.objects.select_for_update().get(pk=product.pk)
        product.quantity -= quantity
        product.save()
    def _add_to_order(self, order):
        user = self.context['request'].user
        cart = UserCart.objects.get(user=user)
        items = Cart.objects.filter(cart=cart)
        total = 0
        with transaction.atomic():
            for item in items:
                if item.product.quantity < item.quantity:
                    raise serializers.ValidationError('quantity is less than product quantity')
                if item.product.is_active == False or item.product.is_deleted == True or item.product.quantity == 0:
                    raise serializers.ValidationError('product is not active or available')
                self._buy_product(item.product, item.quantity)
                Order.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                total += item.product.price * item.quantity
        return total

    def create(self, validated_data):
        user_order = UserOrder.objects.create(**validated_data)
        total = self._add_to_order(user_order)
        user_order.total_amount = total
        user_order.save()
        return user_order
