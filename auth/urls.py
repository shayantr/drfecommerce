from django.urls import path, include
from rest_framework import routers

from auth.api.user import LoginApiView, RegisterApiView
app_name = 'auth'

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path("register/", RegisterApiView.as_view(), name="register"),
]