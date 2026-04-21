from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from auth.api.login.serializers import AdminSerializer
from core.models import User


class AdminUserLoginAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminSerializer
    queryset = User.objects.all()