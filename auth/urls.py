from django.urls import path, include
from rest_framework import routers

from auth.api.admin import AdminUserLoginAPIView
from auth.api.user import UserLoginApiView, UserRegisterApiView
app_name = 'auth'

urlpatterns = [
    path('admin-token/', AdminUserLoginAPIView.as_view()),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path("register/", UserRegisterApiView.as_view(), name="register"),
]