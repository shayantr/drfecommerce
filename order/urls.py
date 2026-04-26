from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.api.admin import OrderViewSet, PaymentViewSet, OrderDetailViewSet
from order.api.user import AddToCartViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r"order-details", OrderDetailViewSet, basename='order-details')
router.register(r'payments', PaymentViewSet)
router.register(r'carts', AddToCartViewSet, basename='carts')
app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
]