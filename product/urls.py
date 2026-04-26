from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.admin import ProductApiViewSet, CreateImageApiView
from product.api.user import ProductViewSet, ProductDetailViewSet

app_name = 'product'
router = DefaultRouter()
router.register('admin-products', ProductApiViewSet, basename='admin-products')
router.register('products', ProductViewSet)
router.register('product_details', ProductDetailViewSet, basename='product-details')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', CreateImageApiView.as_view(), name='upload-image'),
]

