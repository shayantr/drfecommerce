from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.admin_product import ProductApiViewSet, CreateImageApiView

app_name = 'product'
router = DefaultRouter()
router.register('products', ProductApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', CreateImageApiView.as_view(), name='upload-image'),
]

