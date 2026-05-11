from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Cart
from core.utills.permissions import AuthenticatedUserViewSet
from purchase.api.user.cart.serializers import AddToCartSerializer, UpdateCartSerializer


class AddToCartViewSet(AuthenticatedUserViewSet, ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = UpdateCartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return AddToCartSerializer
        return super(AddToCartViewSet, self).get_serializer_class()

    def get_queryset(self):
        return Cart.objects.select_related('product', 'cart__user').filter(cart__user=self.request.user)