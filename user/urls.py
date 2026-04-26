from django.urls import include, path
from rest_framework import routers

from user.api.user import DetailAddressViewSet, ListUserAddressViewSet

router = routers.DefaultRouter()
router.register('address', DetailAddressViewSet)
router.register('address-list', ListUserAddressViewSet, basename='address-list')

urlpatterns = [
    path('', include(router.urls)),
]