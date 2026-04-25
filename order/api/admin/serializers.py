from rest_framework import serializers

from core.models import Order, UserOrder, Payment, UserAddress
from core.models.order import OrderStatus


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Order
        fields = ["id", "product", "quantity", "price"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['name', 'last_name', 'street', 'city', 'post_code', 'province', 'details']


class AdminUserOrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='address.name', read_only=True)
    last_name = serializers.CharField(source='address.last_name', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'name', 'last_name', 'status', 'total_amount', 'created_at']

    def update(self, instance, validated_data):
        status = validated_data.pop('status')
        instance.status = status
        instance.save()
        return instance


class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='address.name', read_only=True)
    last_name = serializers.CharField(source='address.last_name', read_only=True)
    items = OrderSerializer(source='orders', read_only=True, many=True)
    address = AddressSerializer(read_only=True)
    status = serializers.ChoiceField(choices=OrderStatus.values, read_only=True)

    class Meta:
        model = UserOrder
        fields = ['id', 'name', 'last_name', 'status', 'total_amount', 'created_at', 'address', "items"]


class AdminPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(read_only=True)
    ip_address = serializers.CharField(read_only=True)
    transaction_id = serializers.CharField(read_only=True)
    gateway = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "amount", "status", "ip_address", "transaction_id", "gateway"]

    def update(self, instance, validated_data):
        status = validated_data.pop('status')
        instance.status = status
        instance.save()

        return instance
