from rest_framework.permissions import BasePermission

from core.models.user import RoleStatus


class IsAdminProvider(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.rol == RoleStatus.ADMIN