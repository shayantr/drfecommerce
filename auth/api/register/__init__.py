from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from auth.api.register.serializers import RegisterSerializer


class RegisterApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer