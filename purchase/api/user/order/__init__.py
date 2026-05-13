from rest_framework import viewsets, mixins
from core.models import UserOrder
from core.utills.permissions import AuthenticatedUserViewSet
from purchase.api.user.order.serializers import UserOrderSerializer, UserOrderDetailSerializer


class UserOrderViewSet(AuthenticatedUserViewSet, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = UserOrder.objects.all()
    serializer_class = UserOrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserOrderDetailSerializer
        return UserOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


