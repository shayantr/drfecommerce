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

    def validate_user_order(self, user_order):
        if user_order.status != OrderStatus.AWAITING_PAYMENT:
            raise serializers.ValidationError('order is not on AWAITING PAYMENT')
        return user_order

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
        ip = get_client_ip(self.context.get('request'))
        gateway = ZarinGatWay(user_order=user_order, ip=ip)
        res = gateway.request()
        if not res['success']:
            raise serializers.ValidationError(res['error'])
        return res['payment']
