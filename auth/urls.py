from django.urls import path

from auth.api.login import AdminUserLoginAPIView

urlpatterns = [
    path('admin-token/', AdminUserLoginAPIView.as_view()),
]