from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from core.models import UserOrder
from core.utils.permissions import AuthenticatedUserViewSet
from purchase.api.user.order.serializers import AddOrderSerializer, UserOrderDetailSerializer

@extend_schema(
    tags=['order'],
)
class UserOrderViewSet(AuthenticatedUserViewSet, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = UserOrder.objects.all()
    serializer_class = AddOrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserOrderDetailSerializer
        return AddOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


