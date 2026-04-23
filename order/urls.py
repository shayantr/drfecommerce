from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.api.admin import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
]