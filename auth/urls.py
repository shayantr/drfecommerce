from django.urls import path

from auth.api.Login import AdminUserLoginAPIView

urlpatterns = [
    path('admin-token/', AdminUserLoginAPIView.as_view()),
]