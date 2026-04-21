from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from auth.api.Login import serializers


class AdminUserLoginAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.AdminSerializer
