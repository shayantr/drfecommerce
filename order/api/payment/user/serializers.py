from rest_framework import serializers

from order.gatway import ZarinGatWay
from core.models import Payment
from core.models.order import OrderStatus
from core.utills import get_client_ip


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'status', 'ip_address', 'transaction_id', 'gateway', 'link']
        read_only_fields = ['id', 'user', 'amount', 'status', 'gateway', 'transaction_id', 'gateway', 'ip_address', 'link']

    def validate_order(self, order):
        if order.status != OrderStatus.PENDING:
            raise serializers.ValidationError('order is not on pending')
        return order

    def create(self, validated_data):
        order = validated_data['order']
        payment = Payment.objects.filter(order=order, status=1)
        if payment.exists():
            return payment.first()
        gateway = ZarinGatWay(order=order)
        ip = get_client_ip(self.context.get('request'))
        res = gateway.request()
        transaction_id = res['authority']
        link = gateway.get_link()
        payment = Payment.objects.create(
            **validated_data,
            transaction_id=transaction_id,
            amount=order.total_amount,
            gateway=gateway,
            ip_address=ip,
            link=link
        )
        return payment
