from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models.user import Roles


class IsAdminProvider(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role == Roles.ADMIN

class AdminAuthentication(GenericViewSet):
    permission_classes = [IsAdminProvider]
    authentication_classes = [JWTAuthentication]

class AuthenticatedUserViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]