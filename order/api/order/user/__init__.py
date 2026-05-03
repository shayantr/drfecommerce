from rest_framework import viewsets, mixins

from core.models import UserOrder
from core.views import AuthenticatedUserViewSet
from order.api.order.user.serializers import UserOrderSerializer


class UserOrderViewSet(AuthenticatedUserViewSet, viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = UserOrder.objects.all()
    serializer_class = UserOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)