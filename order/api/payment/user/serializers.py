from rest_framework import serializers

from core.gatway import ZarinGatWay
from core.models import Payment
from core.utills import get_client_ip


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'status', 'ip_address', 'transaction_id', 'gateway']
        read_only_fields = ['id', 'user', 'amount', 'status', 'gateway', 'transaction_id', 'gateway', 'ip_address']

    def create(self, validated_data):
        order = validated_data['order']
        gateway = ZarinGatWay(order=order)
        ip = get_client_ip(self.context.get('request'))
        res = gateway.request()
        transaction_id = res['data']['authority']
        payment = Payment.objects.create(**validated_data, transaction_id=transaction_id, amount=order.total_amount, gateway=gateway, ip_address=ip)
        return payment

