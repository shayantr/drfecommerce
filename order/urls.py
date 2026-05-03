from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.api.cart import AddToCartViewSet
from order.api.order.admin import AdminOrderViewSet, AdminOrderDetailViewSet, AdminPaymentViewSet
from order.api.order.user import UserOrderViewSet
from order.api.payment.user import PaymentModelViewSet

router = DefaultRouter()
router.register(r'admin-orders', AdminOrderViewSet, basename='admin-orders')
router.register(r"admin-order-details", AdminOrderDetailViewSet, basename='admin-order-details')
router.register(r'admin-payments', AdminPaymentViewSet, 'admin-payments')
router.register(r'carts', AddToCartViewSet, basename='carts')
router.register(r'create-order', UserOrderViewSet, basename='create-order')
router.register(r'payments', PaymentModelViewSet, basename='payment')
app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
]