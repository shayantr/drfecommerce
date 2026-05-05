from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from order.gatway import ZarinGatWay
from core.models import Payment
from order.api.payment.user.serializers import PaymentSerializer


class PaymentModelViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PaymentSerializer
    model = Payment

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def call_back(self, request: Request, *args, **kwargs):
        authority = request.query_params.get('Authority')
        status = request.query_params.get('Status')

        if not authority:
            return Response({'error': 'Authority missing'}, status=400)

        payment = Payment.objects.get(transaction_id=authority)

        gateway = ZarinGatWay(order=payment.order)
        result = gateway.verify(authority=authority, status=status)
        payment.status = result
        payment.save()

        return Response(result)

