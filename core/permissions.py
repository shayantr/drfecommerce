from rest_framework.permissions import BasePermission

from core.models.choices import AuthProviders


class IsAdminProvider(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.auth_providers == AuthProviders.ADMIN