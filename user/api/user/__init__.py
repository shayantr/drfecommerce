from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.models import UserAddress
from core.views import AuthenticatedUserViewSet
from user.api.user.serializers import AddressSerializer, AddressListSerializer


class DetailAddressViewSet(AuthenticatedUserViewSet, ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AddressListSerializer
        return self.serializer_class

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
