from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Product, ProductImage
from product.api.admin_product.serializers import AdminProductSerializer, ImageProductSerializer


class ProductApiViewSet(ModelViewSet):
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'


class CreateImageApiView(generics.CreateAPIView):
    serializer_class = ImageProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


