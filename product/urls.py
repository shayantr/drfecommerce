from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.admin_product import ProductApiModelViewSet
app_name = 'product'
router = DefaultRouter()
router.register('products', ProductApiModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]

