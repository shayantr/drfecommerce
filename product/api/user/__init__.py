import django_filters
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny

from core.models import Product
from product.api.user.serializers import ProductSerializer, ProductDetailSerializer


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    available = django_filters.BooleanFilter(field_name="is_active")

    exclude_category = django_filters.BaseInFilter(field_name='categories__slug', lookup_expr='in', exclude=True)
    multi_categories = django_filters.BaseInFilter(field_name='categories__slug', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['title']

class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny,]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']



    def get_queryset(self):
        return Product.objects.all().prefetch_related("images", "categories").order_by('is_active')


class ProductDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images")



