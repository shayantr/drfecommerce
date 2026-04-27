from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import UserAddress
from user.api.user.serializers import AddressSerializer, AddressListSerializer


class DetailAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'list':
            return AddressListSerializer
        return self.serializer_class

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
