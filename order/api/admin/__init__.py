from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Order, UserOrder
from order.api.admin.serializers import UserOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

