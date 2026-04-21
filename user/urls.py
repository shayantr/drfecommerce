from django.urls import include, path
from rest_framework import routers

from auth.api.admin_login.views import AdminUserLoginAPIView
from user import views


router = routers.DefaultRouter()
router.register(r'users', views.UserListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin-token/', AdminUserLoginAPIView.as_view()),
]