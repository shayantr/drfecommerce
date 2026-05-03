from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.gatway import ZarinGatWay
from core.models import Payment
from core.views import AuthenticatedUserViewSet
from order.api.payment.user.serializers import PaymentSerializer




class PaymentModelViewSet(AuthenticatedUserViewSet, GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PaymentSerializer
    model = Payment

    @action(detail=False, methods=['get'])
    def call_back(self, request: Request, *args, **kwargs):
        authority = request.query_params.get('Authority')
        status = request.query_params.get('Status')

        if not authority:
            return Response({'error': 'Authority missing'}, status=400)

        payment = Payment.objects.get(transaction_id=authority)

        gateway = ZarinGatWay(order=payment.order)
        result = gateway.verify(authority=authority, status=status, payment=payment)

        return Response(result)




