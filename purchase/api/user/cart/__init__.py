from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Cart, UserCart
from core.utils.permissions import AuthenticatedUserViewSet
from purchase.api.user.cart.serializers import AddToCartSerializer, UpdateCartSerializer, ListCartSerializer
from purchase.api.user.discount.serializers import ApplyDiscountSerializer


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
        if self.action == 'update':
            return UpdateCartSerializer
        if self.action == 'apply_discount':
            return ApplyDiscountSerializer
        return super(AddToCartViewSet, self).get_serializer_class()

    @action(detail=False, methods=["patch"], url_path="apply-discount")
    def apply_discount(self, request):
        user_cart = self.get_queryset().first()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ListCartSerializer(user_cart, many=False).data)

    def get_queryset(self):
        if self.action in ['list', 'apply_discount']:
            return UserCart.objects.prefetch_related('items', 'items__product').filter(user=self.request.user)
        return Cart.objects.select_related('product', 'user_cart__user').filter(user_cart__user=self.request.user)

