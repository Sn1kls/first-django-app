from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsAdminOrManager(BasePermission):
    """
    Allows access only to administrators and managers.
    """
    def has_permission(self, request, view):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MANAGER]
