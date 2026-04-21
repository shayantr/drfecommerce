from django.urls import path

from auth.api.admin_login.views import AdminUserLoginAPIView

urlpatterns = [
    path('admin-token/', AdminUserLoginAPIView.as_view()),
]