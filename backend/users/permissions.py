from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с is_admin=True."""
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.is_admin
        )