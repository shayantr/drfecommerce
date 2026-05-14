from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.models import UserAddress
from core.utils.permissions import AuthenticatedUserViewSet
from core.utils.shared_serializers import AddressSerializer
from user.api.user.serializers import AddressListSerializer

@extend_schema(
    tags=['address']
)
class DetailAddressViewSet(AuthenticatedUserViewSet, ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AddressListSerializer
        return self.serializer_class

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
