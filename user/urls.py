from django.urls import include, path
from rest_framework import routers

from user.api.user import DetailAddressViewSet

router = routers.DefaultRouter()
router.register('address', DetailAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]