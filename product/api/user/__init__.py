from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from core.models import Product
from product.api.user.serializers import ProductSerializer, ProductDetailSerializer


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images")

class ProductDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images")

