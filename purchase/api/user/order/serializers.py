from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DJValidationError

from core.models.discount import DiscountUsage
from core.utils.get_client_ip import get_client_ip
from core.models import Order, Cart, UserOrder, UserCart
from purchase.service.zarin_gateway import ZarinGatWay
from user.api.user import AddressSerializer


class ItemDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Order
        fields = ['product', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.price * obj.quantity


class UserOrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = ItemDetailSerializer(source='orders', many=True, read_only=True)
    address = AddressSerializer(read_only=True, many=False)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'total_amount', 'address', 'items']



class AddOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    link = serializers.CharField(read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'total_amount', 'address', 'link']
        read_only_fields = ('id', 'status', 'total_amount')

    def validate(self, attrs):
        user = attrs.get('user')
        user_cart = UserCart.objects.filter(user=user)
        if not user_cart.exists():
            raise serializers.ValidationError('cart is empty')
        user_cart = user_cart.prefetch_related('items').first()
        attrs['user_cart'] = user_cart
        for item in user_cart.items.all():
            if item.product.quantity < item.quantity:
                raise serializers.ValidationError('quantity is less than product quantity')
            if item.product.is_active == False or item.product.is_deleted == True or item.product.quantity == 0:
                raise serializers.ValidationError('product is not active or available')
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user_cart = validated_data.pop('user_cart')
            user_order = UserOrder.objects.create(**validated_data)
            try:
                total, discount = user_order.save_cart_to_order(user_cart)
            except ValueError as e:
                raise ValidationError(str(e))
            user_order.discount = discount
            user_order.total_amount = total
            user_order.discount_amount = discount.calculate_discount(total)
            user_order.final_amount = total - user_order.discount_amount
            user_order.save()
            DiscountUsage.objects.create(
                user=validated_data['user'],
                discount=discount,
                user_order=user_order,
            )
            ip = get_client_ip(self.context.get('request'))
            gateway = ZarinGatWay(user_order, ip)
            res = gateway.request()
            if not res['success']:
                raise serializers.ValidationError(res['error'])

        return {
            'total_amount': total,
            'address': user_order.address,
            'link': gateway.get_link(res['data']['authority'])
        }
