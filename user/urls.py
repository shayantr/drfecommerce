from django.urls import include, path
from rest_framework import routers

from user import views
from user.views import AdminUserLoginAPIView

router = routers.DefaultRouter()
router.register(r'users', views.UserListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin-token/', AdminUserLoginAPIView.as_view()),
]