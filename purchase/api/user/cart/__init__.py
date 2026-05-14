from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from core.models import Cart, UserCart
from core.utils.permissions import AuthenticatedUserViewSet
from purchase.api.user.cart.serializers import AddToCartSerializer, UpdateCartSerializer, ListCartSerializer

@extend_schema(
    tags=['Cart'],
)
@extend_schema_view(
    create=extend_schema(
        description='Add Product ID and the quantity that client requested'),
    list=extend_schema(description='return products name, quantities and total prices with final price'),
)
class AddToCartViewSet(AuthenticatedUserViewSet, ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = UpdateCartSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AddToCartSerializer
        if self.action == 'list':
            return ListCartSerializer
        return super(AddToCartViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.action == 'list':
            return UserCart.objects.prefetch_related('items', 'items__product').filter(user=self.request.user)
        return Cart.objects.select_related('product', 'cart__user').filter(cart__user=self.request.user)