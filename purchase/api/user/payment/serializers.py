from rest_framework import serializers

from core.models.payment import PaymentStatus
from core.utills.get_client_ip import get_client_ip
from purchase.gatway import ZarinGatWay
from core.models import Payment
from core.models.order import OrderStatus, UserOrder


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'status', 'ip_address', 'transaction_id', 'gateway', 'link']
        read_only_fields = ['id', 'user', 'amount', 'status', 'gateway', 'transaction_id', 'gateway', 'ip_address',
                            'link']

    def validate_order(self, order):
        if order.status != OrderStatus.AWAITING_PAYMENT:
            raise serializers.ValidationError('order is not on AWAITING PAYMENT')
        return order

    def create(self, validated_data):
        order = UserOrder.objects.select_for_update().get(id=validated_data['order'].id)
        payment = Payment.objects.filter(order=order)
        pending_payment = payment.filter(
            status=PaymentStatus.PENDING
        ).first()
        if pending_payment:
            return pending_payment
        if payment.filter(status=PaymentStatus.PAID).exists():
            raise serializers.ValidationError('payment is already paid')
        gateway = ZarinGatWay(order=order)
        ip = get_client_ip(self.context.get('request'))
        res = gateway.request()
        transaction_id = res['authority']
        link = gateway.get_link(transaction_id)
        payment = Payment.objects.create(
            **validated_data,
            transaction_id=transaction_id,
            amount=order.total_amount,
            gateway=gateway,
            ip_address=ip,
            link=link
        )
        return payment
