from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models.order import OrderStatus
from core.models.payment import PaymentStatus
from purchase.gatway import ZarinGatWay
from core.models import Payment, UserOrder
from purchase.api.user.payment.serializers import PaymentSerializer


class PaymentModelViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PaymentSerializer
    model = Payment

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], authentication_classes=[])
    def call_back(self, request: Request, *args, **kwargs):
        authority = request.query_params.get('Authority')
        status = request.query_params.get('Status')

        if not authority:
            return Response({'error': 'Authority missing'}, status=400)
        if status == "OK" or 'OKback':
            try:
                payment = Payment.objects.select_related('order').get(transaction_id=authority)
                gateway = ZarinGatWay(order=payment.order)
                result = gateway.verify(authority=authority)
                payment.order.status = OrderStatus.PENDING
                payment.order.save(update_fields=['status'])
                payment.status = PaymentStatus.PAID
                payment.save(update_fields=['status'])
                return Response({'result': result}, status=200)
            except Payment.DoesNotExist:
                return Response({"error": 'Payment not found'}, status=404)
            except:
                return Response(result, status=400)
        else:
            return Response({'error': 'Authority failed'}, status=400)
