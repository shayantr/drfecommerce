from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from auth.api.login.serializers import LoginSerializer


class LoginApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer