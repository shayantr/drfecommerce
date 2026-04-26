from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Cart, UserCart
from order.api.user.serializers import AddToCartSerializer


class AddToCartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Cart.objects.select_related('product', 'cart__user').filter(cart__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        final_price = 0
        for s in serializer.data:
            final_price += s['total_price']
        return Response({
            'results': serializer.data,
            'final_price': final_price
        })