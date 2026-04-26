from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.api.user.serializers import LoginSerializer, RegisterSerializer
from core.models import User


class UserLoginApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

class UserRegisterApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

