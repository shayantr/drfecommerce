from rest_framework import viewsets

from core.models.category import Category
from core.utils.permissions import AdminAuthentication
from product.api.admin.category.serializers import CategorySerializer


class CategoryApiViewSet(AdminAuthentication,viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
