from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models.order import OrderStatus
from core.models.payment import PaymentStatus
from core.models import Payment, UserOrder
from purchase.api.user.payment.serializers import PaymentSerializer
from purchase.service.zarin_gateway import ZarinGatWay

@extend_schema(
    tags=['payment'],
)
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
                payment = Payment.objects.select_related('user_order').get(authority_id=authority)
                gateway = ZarinGatWay(user_order=payment.user_order)
                result = gateway.verify(authority=authority)
                payment.user_order.status = OrderStatus.PENDING
                payment.user_order.save(update_fields=['status'])
                payment.status = PaymentStatus.PAID
                payment.transaction_id = result['data']['ref_id']
                payment.save(update_fields=['status'])
                return Response({'result': result}, status=200)
            except Payment.DoesNotExist:
                return Response({"error": 'Payment not found'}, status=404)
            except:
                return Response(result, status=400)
        else:
            return Response({'error': 'Authority failed'}, status=400)
