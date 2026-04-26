from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from core.models import User
from core.permissions import IsAdminProvider
from user.api.admin.serializers import UserSerializer


class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminProvider]
