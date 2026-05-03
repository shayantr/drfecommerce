from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Cart
from order.api.cart.serializers import AddToCartSerializer


class AddToCartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Cart.objects.select_related('product', 'cart__user').filter(cart__user=self.request.user)

