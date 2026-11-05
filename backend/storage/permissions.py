from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешает доступ владельцу объекта или администратору (is_admin=True).
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.owner == request.user