from django.db import transaction
from rest_framework import serializers

from core.utils.get_client_ip import get_client_ip
from core.models import Order, Cart, UserOrder, UserCart, Product, Payment
from purchase.service.zarin_gateway import ZarinGatWay
from user.api.user import AddressSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Order
        fields = ['product', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.price * obj.quantity


class UserOrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderDetailSerializer(source='orders', many=True, read_only=True)
    address = AddressSerializer(read_only=True, many=False)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'total_amount', 'address', 'items']



class UserOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    link = serializers.CharField(read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'total_amount', 'address', 'link']
        read_only_fields = ('id', 'status', 'total_amount')

    def _buy_product(self, product, quantity):
        product = Product.objects.select_for_update().get(pk=product.pk)
        product.quantity -= quantity
        product.save()

    def validate(self, attrs):
        user = attrs.get('user')
        user_cart = UserCart.objects.filter(user=user)
        if not user_cart.exists():
            raise serializers.ValidationError('cart is empty')
        else:
            user_cart = user_cart.first()
        items = Cart.objects.filter(user_cart=user_cart)
        for item in items:
            if item.product.quantity < item.quantity:
                raise serializers.ValidationError('quantity is less than product quantity')
            if item.product.is_active == False or item.product.is_deleted == True or item.product.quantity == 0:
                raise serializers.ValidationError('product is not active or available')
        return attrs

    def _add_to_order(self, user_order):
        user = self.context['request'].user
        user_cart = UserCart.objects.get(user=user)
        items = Cart.objects.filter(user_cart=user_cart)
        total = 0
        for item in items:
            self._buy_product(item.product, item.quantity)
            if item.product.sale_price:
                Order.objects.create(
                    user_order=user_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.sale_price
                )
                total += item.product.sale_price * item.quantity
            else:
                Order.objects.create(
                    user_order=user_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                total += item.product.price * item.quantity
        user_cart.delete()
        return total

    def create(self, validated_data):
        with transaction.atomic():
            user_order = UserOrder.objects.create(**validated_data)
            user = user_order.user
            total = self._add_to_order(user_order)
            user_order.total_amount = total
            user_order.save()
            gateway = ZarinGatWay(user_order)
            res = gateway.request()
            if not res['success']:
                raise serializers.ValidationError(res['error'])
            ip = get_client_ip(self.context.get('request'))
            Payment.objects.create(
                user=user,
                link=gateway.get_link(res['data']['authority']),
                authority=res['data']['authority'],
                user_order=user_order,
                amount=total,
                gateway=gateway,
                status=1,
                ip_address=ip
            )

        return {
            'total_amount': total,
            'address': user_order.address,
            'link': gateway.get_link(res['data']['authority'])
        }
