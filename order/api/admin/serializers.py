from django.db import transaction
from rest_framework import serializers

from core.models import Order, Product, UserOrder


# class OrderSerializer(serializers.ModelSerializer):
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
#     price = serializers.IntegerField(read_only=True, required=False)
#     quantity = serializers.IntegerField(required=False)
#
#     class Meta:
#         model = Order
#         fields = ['product', 'price', 'quantity']
#
#     def validate_product(self, product):
#         if not product.is_active or product.is_deleted or product.quantity < 1:
#             raise serializers.ValidationError('no product available')
#         return product
#     def validate_quantity(self, quantity):
#         if quantity < 1:
#             raise serializers.ValidationError('quantity must be greater than 0')
#         return quantity
#
#     def create(self, validated_data):
#         product = validated_data['product']
#         quantity = validated_data['quantity']
#         with transaction.atomic():
#             product = Product.objects.select_for_update().get(product=product)
#             order = Order.objects.create(**validated_data)
#             order.price = product.price
#             order.quantity = quantity
#             if product.quantity > order.quantity:
#                 product.quantity -= order.quantity
#                 product.save()
#                 order.save()
#             else:
#                 raise serializers.ValidationError('quantity must be greater than product quantity')
#         return order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "product", "quantity", "price"]

class UserOrderSerializer(serializers.ModelSerializer):
    orders_list = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True, many=True)
    orders = OrderSerializer(read_only=True, many=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'status', 'total_amount', 'address', 'orders', 'orders_list']

    def create(self, validated_data):
        orders = validated_data.pop('orders_list')
        user = self.context['request'].user
        with transaction.atomic():
            user_order = UserOrder.objects.create(**validated_data, user=user)
            for order in orders:
                user_order.orders.add(order)
            user_order.save()
        return user_order

    def update(self, instance, validated_data):
        status = validated_data.pop('status')
        instance.status = status
        instance.save()
        return instance



