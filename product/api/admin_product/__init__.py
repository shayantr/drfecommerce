from rest_framework import mixins, generics
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Product, ProductImage
from product.api.admin_product.serializers import AdminProductSerializer, ImageProductSerializer


class ProductApiModelViewSet(ModelViewSet):
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreateImageApiView(generics.CreateAPIView):
    serializer_class = ImageProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

