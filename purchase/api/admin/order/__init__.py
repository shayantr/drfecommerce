from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import UserOrder, Payment
from purchase.api.admin.order.serializers import AdminUserOrderSerializer, OrderDetailSerializer, AdminPaymentSerializer


class AdminOrderViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = AdminUserOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.all().prefetch_related('address')

class AdminOrderDetailViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.all().select_related('address').prefetch_related('orders')



class AdminPaymentViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = AdminPaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
