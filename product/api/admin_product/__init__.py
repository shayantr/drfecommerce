from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Product
from product.api.admin_product.serializers import AdminProductSerializer


class CreateProductApiView(CreateAPIView):
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



