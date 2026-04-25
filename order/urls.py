from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.api.admin import OrderViewSet, PaymentViewSet, OrderDetailViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r"order-details", OrderDetailViewSet, basename='order-details')
router.register(r'payments', PaymentViewSet)
app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
]