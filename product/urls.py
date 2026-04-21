from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.admin_product import CreateProductApiView, ProductApiModelViewSet

router = DefaultRouter()
router.register('products', ProductApiModelViewSet)

urlpatterns = [
    path('list/', CreateProductApiView.as_view()),
    path('', include(router.urls))
]

