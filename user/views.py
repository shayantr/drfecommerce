from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from core.models import User
from core.permissions import IsAdminProvider
from user.serializers import UserSerializer, AdminSerializer


# Create your views here.

class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminProvider]

