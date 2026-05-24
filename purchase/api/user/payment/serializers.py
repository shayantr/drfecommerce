from rest_framework import serializers

from core.models.payment import PaymentStatus
from core.utils.get_client_ip import get_client_ip
from core.models import Payment
from core.models.order import OrderStatus, UserOrder
from purchase.service.zarin_gateway import ZarinGatWay


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_order', 'amount', 'status', 'ip_address', 'transaction_id', 'gateway', 'link']
        read_only_fields = ['id', 'user', 'amount', 'status', 'gateway', 'transaction_id', 'gateway', 'ip_address',
                            'link']

    def validate_order(self, order):
        if order.status != OrderStatus.AWAITING_PAYMENT:
            raise serializers.ValidationError('order is not on AWAITING PAYMENT')
        return order

    def create(self, validated_data):
        user_order = UserOrder.objects.select_for_update().get(id=validated_data['user_order'].id)
        payment = Payment.objects.filter(user_order=user_order)
        pending_payment = payment.filter(
            status=PaymentStatus.PENDING
        ).first()
        if pending_payment:
            return pending_payment
        if payment.filter(status=PaymentStatus.PAID).exists():
            raise serializers.ValidationError('payment is already paid')
        gateway = ZarinGatWay(user_order=user_order)
        ip = get_client_ip(self.context.get('request'))
        res = gateway.request()
        if not res['success']:
            raise serializers.ValidationError(res['error'])
        authority = res['data']['authority']
        link = gateway.get_link(authority)
        payment = Payment.objects.create(
            **validated_data,
            authority=authority,
            amount=user_order.total_amount,
            gateway=gateway,
            ip_address=ip,
            link=link
        )
        return payment
