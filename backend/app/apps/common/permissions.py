from rest_framework.permissions import BasePermission

from apps.users.models import User


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user: User | None = getattr(request, "user", None)
        return bool(
            user and user.is_authenticated and user.role in (User.Role.MANAGER, User.Role.ADMIN)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user: User | None = getattr(request, "user", None)
        return bool(user and user.is_authenticated and user.role == User.Role.ADMIN)
