from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import UserAddress
from user.api.user.serializers import AddressSerializer, AddressListSerializer


class ListUserAddressViewSet(ListModelMixin, GenericViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

class DetailAddressViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
