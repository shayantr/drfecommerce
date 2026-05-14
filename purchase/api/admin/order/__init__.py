from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.models import UserOrder, Payment
from core.utils.permissions import AdminAuthentication
from purchase.api.admin.order.serializers import AdminUserOrderSerializer, AdminOrderDetailSerializer, AdminPaymentSerializer


class AdminOrderViewSet(
    AdminAuthentication,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = AdminUserOrderSerializer

    def get_queryset(self):
        return self.queryset.all().prefetch_related('address')

class AdminOrderDetailViewSet(AdminAuthentication, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = AdminOrderDetailSerializer


    def get_queryset(self):
        return self.queryset.all().select_related('address').prefetch_related('orders')



class AdminPaymentViewSet(AdminAuthentication, mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = AdminPaymentSerializer
