from django.urls import path, include
from rest_framework.routers import DefaultRouter

from purchase.api.admin.order import AdminOrderViewSet, AdminOrderDetailViewSet, AdminPaymentViewSet
from purchase.api.user.cart import AddToCartViewSet
from purchase.api.user.order import UserOrderViewSet
from purchase.api.user.payment import PaymentModelViewSet

router = DefaultRouter()
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-orders')
router.register(r"admin/order-details", AdminOrderDetailViewSet, basename='admin-order-details')
router.register(r'admin/payments', AdminPaymentViewSet, 'admin-payments')
router.register(r'carts', AddToCartViewSet, basename='carts')
router.register(r'order', UserOrderViewSet, basename='order')
router.register(r'payments', PaymentModelViewSet, basename='payment')
app_name = 'purchase'
urlpatterns = [
    path('', include(router.urls)),
]
